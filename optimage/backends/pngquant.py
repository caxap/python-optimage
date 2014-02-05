#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .base import BaseImageOptimizer
from ..utils import find_executable_path

__all__ = ['PngQuant']


class PngQuant(BaseImageOptimizer):
    provider = 'pngquant'
    output_format = 'png'
    content_types = ['image/png']
    command = find_executable_path('pngquant')
    _q8_suffix = '-optimage-q8.png'
    options = ['-f', '--ext', _q8_suffix, '--speed', '5']

    def _output_file_name(self):
        dirname = os.path.dirname(self.input_name)
        basename, _ = os.path.splitext(os.path.basename(self.input_name))
        filename = basename + self._q8_suffix
        output_name = os.path.join(dirname, filename)
        return output_name

    def _build_command(self):
        return [self.command] + self.options + [self.input_name]
