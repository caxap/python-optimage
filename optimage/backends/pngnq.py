#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['PngNQ']


class PngNQ(BaseImageOptimizer):
    priority = 20
    provider = 'pngnq'
    output_format = 'png'
    content_types = ['image/png']
    command = find_executable_path('pngnq')
    _nq8_suffix = '-optimage-nq8.png'
    options = ['-n', '256', '-f', '-Qf', '-s5', '-e%s' % _nq8_suffix]

    def _output_file_name(self):
        dirname = os.path.dirname(self.input_name)
        basename, _ = os.path.splitext(os.path.basename(self.input_name))
        filename = basename + self._nq8_suffix
        output_name = os.path.join(dirname, filename)
        return output_name

    def _build_command(self):
        return [self.command] + self.options + [self.input_name]
