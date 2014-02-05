#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['JpegOptim']


class JpegOptim(BaseImageOptimizer):
    provider = 'jpegoptim'
    output_format = 'jpeg'
    content_types = ['image/jpeg']
    command = find_executable_path('jpegoptim')
    options = ['--strip-all', '--all-normal', '-o', '-q']
