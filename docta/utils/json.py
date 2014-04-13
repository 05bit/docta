"""
JSON load util with basic support of //-style comments.
More coplex comments support hint:
http://www.lifl.fr/~riquetd/parse-a-json-file-with-comments.html
"""
from __future__ import absolute_import, print_function, unicode_literals
import json


def load(stream):
    data = []
    for line in stream:
        if line.strip().startswith('//'):
            data.append('\n')
        else:
            data.append(line)
    return json.loads(''.join(data))
