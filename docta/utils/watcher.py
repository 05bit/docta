"""
Watch & rebuild project utils.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import sys
import time
import watchdog.observers
import watchdog.events
import docta.utils.log as log
import docta.utils.fs as fs

WATCH_PATTERNS_DEFAULT = ['*.html', '*.md']


def watch(project):
    log.message("Watching directory: %s" % project.input_dir())
    observer = watchdog.observers.Observer()
    observer.schedule(ProjectEventHandler(project),
                      project.input_dir(),
                      recursive=True)
    observer.start()
    return observer


class ProjectEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, project, *args, **kwargs):
        self.project = project
        self.config = self.project.config.copy()
        super().__init__(*args, **kwargs)
        log.message("Watching patterns: %s" % ' '.join(self.get_patterns()))

    def get_patterns(self):
        return (self.config
            .setdefault('server', {})
            .setdefault('watch', WATCH_PATTERNS_DEFAULT))

    def on_any_event(self, event):
        log.message(event)
