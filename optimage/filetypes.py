#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

__all__ = ['UNKNOWN_CONTENT_TYPE', 'mime_from_file']


UNKNOWN_CONTENT_TYPE = 'application/x-unknown'


def _check_output_head(args):
    """
    Utility function to get first line of stripped output for given command.
    """
    try:
        output = subprocess.check_output(
            args, stderr=subprocess.STDOUT, shell=False)
        head = output.splitlines()[0] if output else ''
        return head.strip()
    except (subprocess.CalledProcessError, OSError) as e:
        print "Failed to get output for '%s': %s" % (args, e)


def _file_mime_from_file(filename, mime=True):
    """
    Get file mime type using `file` shell commnd.
    """
    if not os.path.exists(filename):
        raise IOError("File does not exist: %s" % (filename, ))

    args = ['file', '-b', '--mime', filename]
    mimetype = _check_output_head(args)
    if mimetype:
        return re.split(r'[:;]\s+', mimetype.strip(), 1)[0]
    return UNKNOWN_CONTENT_TYPE


try:
    import magic as _magic
except ImportError:
    _magic = None  # noqa

if _magic:
    # If python-magic is installed use it as canonical
    # function for mime type detection
    def _magic_mime_from_file(filename, mime=False):
        try:
            return _magic.from_file(filename, mime=mime)
        except _magic.MagicException:
            print "Failed to get magic mime: %s" % (filename, )
            return UNKNOWN_CONTENT_TYPE

    mime_from_file = _magic_mime_from_file
else:
    # Fallback to `file` utility implementation
    mime_from_file = _file_mime_from_file
