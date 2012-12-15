# -*- coding: utf-8 -*-

import re
import os
import json

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)


def parse_s(text):
    """ http://www.lifl.fr/~riquetd/parse-a-json-file-with-comments.html
        Parse a JSON text
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    content = ''.join(text)

    ## Looking for comments
    match = comment_re.search(content)
    while match:
        # single line comment
        content = content[:match.start()] + content[match.end():]
        match = comment_re.search(content)

    # Return json file
    return json.loads(content)


def parse(path):
    if os.path.exists(path):
        with open(path) as f:
            return parse_s(f.read())
    return dict()
