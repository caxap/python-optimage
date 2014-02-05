#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['OptiPng']


class OptiPng(BaseImageOptimizer):
    provider = 'optipng'
    output_format = 'png'
    content_types = ['image/png']
    command = find_executable_path('optipng')
    options = ['-o3', '-quiet']
