#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import mimetypes

from .pngcrush import PngCrush
from .pngnq import PngNQ
from .jpegoptim import JpegOptim
from .jpegtran import JPEGtran
from .gifsicle import Gifsicle

__all__ = ['get_backends_for_content_type']


default_backend_classes = [
    # image/png
    PngNQ, PngCrush,

    # image/jpeg
    JpegOptim, JPEGtran,

    # image/gif
    Gifsicle,
]


def get_backends_for_content_type(input_name, content_type=None,
                                  backend_classes=None, **kwargs):
    if not content_type:
        content_type = mimetypes.guess_type(input_name)[0]

    if not content_type:
        return []

    if not backend_classes:
        backend_classes = default_backend_classes

    backends = []
    for cls in backend_classes:
        if (inspect.isclass(cls) and hasattr(cls, 'content_types') and
                content_type in cls.content_types):
            backends.append(cls(**kwargs))

    backends.sort(key=lambda x: x.priority, reverse=True)
    return backends
