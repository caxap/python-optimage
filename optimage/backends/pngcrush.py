#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['PngCrush']


class PngCrush(BaseImageOptimizer):
    provider = 'pngcrush'
    output_format = 'png'
    content_types = ['image/png']
    output_temp_file = True
    command = find_executable_path('pngcrush')
    options = ['-rem', 'allb', '-reduce', '-q']  # , '-brute']
