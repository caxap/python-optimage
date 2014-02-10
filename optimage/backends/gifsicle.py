#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['Gifsicle']


class Gifsicle(BaseImageOptimizer):
    priority = 10
    provider = 'gifsicle'
    output_format = 'gif'
    content_types = ['image/gif']
    command = find_executable_path('gifsicle')
    options = ['-o3', '-I', '-w']
