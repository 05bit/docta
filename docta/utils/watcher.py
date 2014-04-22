"""
Watch & rebuild project utils.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import sys
import time
import threading
import watchdog.observers
import watchdog.events as events
import docta.utils.log as log
import docta.utils.fs as fs

# Defaults
WATCH_PATTERNS_DEFAULT = ['*.html', '*.md']
REBUILD_DELAY = 0.5  # in seconds


def watch(project):
    """
    Start watching project input directory to perform automatic builds on changes.
    It doesn't lock thread. Returns `watchdog.observers.Observer` instance.
    """
    log.message("Watching directory: %s" % project.input_dir())
    observer = watchdog.observers.Observer()
    observer.schedule(ProjectEventHandler(project),
                      project.input_dir(),
                      recursive=True)
    observer.start()
    return observer


class ProjectEventHandler(events.FileSystemEventHandler):
    """
    Watches events in project input directory and automatically
    builds it.
    """
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup
        self.project = project
        self.config = self.project.config.copy()
        self.rebuild_timer = None
        self.rebuild_going = False
        self.events_file = (events.FileModifiedEvent, events.FileCreatedEvent, events.FileDeletedEvent)
        self.events_dirs = (events.DirMovedEvent, events.DirDeletedEvent)
        self.ignore_dirs = [self.project.output_dir('html')]
        log.message("Watching ignore: %s" % self.ignore_dirs)
        log.message("Watching patterns: %s" % ' '.join(self.get_patterns()))

        # initial build
        self.build()

    def get_patterns(self):
        """
        Get watched file patterns from project `server:watch` config section.
        Returns a `list` of UNIX-like file masks, e.g. `['*.html', '*.md']`.
        """
        return (self.config
            .setdefault('server', {})
            .setdefault('watch', WATCH_PATTERNS_DEFAULT))

    def is_path_ignored(self, path):
        """
        Check if path is within ignored dirs.
        """
        return any([fs.issub(path, base) for base in self.ignore_dirs])

    def on_any_event(self, event):
        """
        Filter file/dir events and schedule project rebuild.
        """
        if not self.is_path_ignored(event.src_path):
            if isinstance(event, self.events_file):
                name = fs.basename(event.src_path)
                if any([fs.match(name, mask) for mask in self.get_patterns()]):
                    self.log_event("file updated: %s" % event.src_path)
                    self.schedule_build()
            elif isinstance(event, self.events_dirs):
                self.log_event("directory updated: %s" % event.src_path)
                self.schedule_build()

    def schedule_build(self):
        """
        Re(schedule) project build after some delay (500 ms by default). We want
        to make sure all buch of recent events have been dispatched.
        """
        # log.message("Schedule project rebuild")
        if self.rebuild_timer:
            self.rebuild_timer.cancel()
        self.rebuild_timer = threading.Timer(REBUILD_DELAY, self.build)
        self.rebuild_timer.start()

    def build(self):
        """
        Build project and log time spent for operation.
        """
        t0 = time.time()
        if self.rebuild_going:
            self.schedule_build()
        else:
            self.rebuild_going = True
            self.project.build(['html'])
            t1 = time.time()
            self.rebuild_going = False
        self.log_event("rebuild time: %.2fms" % (1000.0 * (t1 - t0)))

    def log_event(self, text):
        """
        Shortcut for nicely formatted event logging.
        """
        log.success("  %s" % text)
