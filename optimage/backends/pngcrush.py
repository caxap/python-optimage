#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['PngCrush']


class PngCrush(BaseImageOptimizer):
    priority = 10
    provider = 'pngcrush'
    output_format = 'png'
    content_types = ['image/png']
    inline = False
    command = find_executable_path('pngcrush')
    options = ['-rem', 'alla', '-brute', '-reduce', '-q']
