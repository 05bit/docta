"""
Documents metadata tools.
"""
from __future__ import absolute_import, print_function, unicode_literals
import yaml

DELIMITER = '---'


def stripped(stream):
    """
    Read stream to strip YAML header, returns stripped data.
    """
    data = []
    meta_started = False
    meta_ended = False

    # TODO: cleaner implementation?
    for next_line in stream:
        if meta_ended:  # done with meta, collecting data
            data.append(next_line)
        else:
            if next_line.startswith(DELIMITER):
                if not meta_started:  # meta start found!
                    meta_started = True
                else:  # meta end found!
                    meta_ended = True
            else:  # meta not found at all
                if not meta_started:
                    data.append(next_line)  # don't lose first line
                    meta_ended = True

    # TODO: Avoid double memory use? Oh yes, I'm aware
    #       of premature optimization :)
    return ''.join(data)


def extract(stream, **defaults):
    """
    Read stream and extract YAML header.
    """
    meta = Meta(**defaults)
    meta.load(stream)
    return meta


class Meta(dict):
    """
    Metadata for Markdown files loaded from YAML headers.
    """
    def load(self, stream):
        meta_data = []
        meta_opened = False
        for next_line in stream:
            if next_line.startswith(DELIMITER):
                if meta_opened:
                    break  # all meta is read, stop reading
                else:
                    meta_opened = True  # meta started
                    continue
            elif not meta_opened:
                break  # no meta found
            else:
                meta_data.append(next_line)

        if meta_data:
            self.update(yaml.full_load(''.join(meta_data)))
