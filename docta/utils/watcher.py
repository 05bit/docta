"""
Watch & rebuild project utils.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import os
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
    observer = ProjectObserver(project)
    observer.start()
    return observer


class ProjectObserver(watchdog.observers.Observer):
    """
    Watches changes in project base directory and automatically
    rebuilds project.
    """
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.rebuild_timer = None
        self.rebuild_going = False

    def start(self, *args, **kwargs):
        """
        Schedule all handlers and start watching thread.
        """
        self.build(initial=True)
        self.schedule_all()
        super().start(*args, **kwargs)

    def schedule_all(self):
        """
        Schedule all project directories handlers.
        """
        log.message("Watching directory: %s" % self.project.input_dir())
        self.schedule(ProjectPathEventHandler(self),
                      self.project.input_dir(),
                      recursive=True)

    def needs_rebuild(self):
        """
        Re(schedule) project rebuild after some delay (500 ms by default). The reason of
        delay is we want to make sure all buch of recent events have been dispatched.
        """
        if self.rebuild_timer:
            self.rebuild_timer.cancel()

        self.rebuild_timer = threading.Timer(REBUILD_DELAY, self.build)
        self.rebuild_timer.start()

    def build(self, initial=False):
        """
        Build project and log time spent for operation.
        """
        if not self.rebuild_going:
            self.rebuild_going = True
            t0 = time.time()

            if not initial:
                self.unschedule_all()
            
            self.project.build(['html'])

            if not initial:
                self.schedule_all()

            t1 = time.time()
            self.rebuild_going = False
            log.success("  %s" % "rebuild time: %.2fms" % (1000.0 * (t1 - t0)))


class ProjectPathEventHandler(events.FileSystemEventHandler):
    """
    Rebuilds project on input project data changes.
    """
    def __init__(self, observer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup
        self.observer = observer
        self.project = observer.project
        self.config = self.project.config.copy()
        self.events_file = (events.FileModifiedEvent, events.FileCreatedEvent, events.FileDeletedEvent)
        self.events_dirs = (events.DirMovedEvent, events.DirDeletedEvent)
        log.message("Watching patterns: %s" % ' '.join(self.get_patterns()))

    def get_patterns(self):
        """
        Get watched file patterns from project `server:watch` config section.
        Returns a `list` of UNIX-like file masks, e.g. `['*.html', '*.md']`.
        """
        return (self.config
            .setdefault('server', {})
            .setdefault('watch', WATCH_PATTERNS_DEFAULT))

    def on_any_event(self, event):
        """
        Filter file/dir events and schedule project rebuild.
        """
        if isinstance(event, self.events_file):
            name = fs.basename(event.src_path)
            if any([fs.match(name, mask) for mask in self.get_patterns()]):
                log.success("  %s" % "file updated: %s" % event.src_path)
                self.observer.needs_rebuild()
        elif isinstance(event, self.events_dirs):
            log.success("  %s" % "directory updated: %s" % event.src_path)
            self.observer.needs_rebuild()
