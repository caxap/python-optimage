#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import mimetypes

from .optipng import OptiPng
from .pngcrush import PngCrush
from .pngout import PngOut
from .pngnq import PngNQ
from .pngquant import PngQuant
from .jpegoptim import JpegOptim
from .jpegtran import JPEGtran
from .gifsicle import Gifsicle

__all__ = ['get_backends_for_content_type']


# TODO: use autodiscover function for backends classes
_default_backend_classes = [
    PngNQ,
    PngQuant,
    OptiPng,
    PngCrush,
    PngOut,
    JpegOptim,
    JPEGtran,
    Gifsicle,
]


def get_backends_for_content_type(input_name, content_type=None,
                                  backend_classes=None, **kwargs):
    if not content_type:
        content_type = mimetypes.guess_type(input_name)[0]

    if not content_type:
        return []

    if not backend_classes:
        backend_classes = _default_backend_classes

    backends = []
    for cls in backend_classes:
        if (inspect.isclass(cls) and hasattr(cls, 'content_types') and
                content_type in cls.content_types):
            backends.append(cls(input_name, **kwargs))

    return backends
