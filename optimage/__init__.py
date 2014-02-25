#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'

from .backends import get_backends_for_content_type

__all__ = ['optimize']


def optimize(input_name, content_type=None, **kwargs):
    backends = get_backends_for_content_type(
        input_name, content_type=content_type, **kwargs)

    for backend in backends:
        backend.optimize(input_name)
