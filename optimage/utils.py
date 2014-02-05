#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__all__ = ['is_executable', 'find_executable_path', 'file_size']


def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def find_executable_path(command, paths=None):
    path = os.environ.get('%s_PATH' % command.upper())
    if not path:
        if not paths:
            # Most commonly used paths to install software
            paths = ['/usr/bin/%s', '/usr/local/bin/%s', '/bin/%s']
            paths = [p % command for p in paths]
        for p in paths:
            if is_executable(p):
                path = p
                break
    return path or command


def file_size(fp):
    # File descriptor
    if hasattr(fp, 'name') and os.path.exists(fp.name):
        return os.path.getsize(fp.name)
    # File name
    if type(fp) == type('') and os.path.exists(fp):
        return os.path.getsize(fp)
    # File buffer
    if hasattr(fp, 'seek') and hasattr(fp, 'tell'):
        pos = fp.tell()
        fp.seek(0, os.SEEK_END)
        size = fp.tell()
        fp.seek(pos)
        return size
    # File wrapper, e.g Django File object
    if hasattr(fp, 'size'):
        return fp.size

    raise ValueError("Unable to determine the file's size: %s" % (fp, ))
