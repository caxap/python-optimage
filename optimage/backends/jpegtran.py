#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['JPEGtran']


class JPEGtran(BaseImageOptimizer):
    provider = 'jpegtran'
    output_format = 'jpeg'
    content_types = ['image/jpeg']
    command = find_executable_path('jpegtran')
    options = ['-copy', 'none', '-progressive']
    output_temp_file = True

    def _build_command(self):
        return [self.command] + self.options + \
            ['-outfile', self.output_name, self.input_name]
