#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['JPEGtran']


class JPEGtran(BaseImageOptimizer):
    priority = 20
    provider = 'jpegtran'
    output_format = 'jpeg'
    content_types = ['image/jpeg']
    inline = False
    command = find_executable_path('jpegtran')
    options = ['-optimise', '-copy', 'none', '-progressive']

    def _build_command(self):
        return [self.command] + self.options + \
            ['-outfile', self.output_name, self.input_name]
