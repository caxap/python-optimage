#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['PngOut']


class PngOut(BaseImageOptimizer):
    provider = 'pngout'
    output_format = 'png'
    content_types = ['image/png']
    output_temp_file = True
    command = find_executable_path('pngout')
    options = ['-y', '-q']
