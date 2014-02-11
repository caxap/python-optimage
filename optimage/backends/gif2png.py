#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

from ..utils import find_executable_path
from .base import BaseImageOptimizer
try:
    import Image
except ImportError:
    Image = None  # noqa


def _PIL_is_animated(image_name):
    img = Image.open(image_name)
    try:
        img.seek(1)
        return True
    except (IOError, EOFError):
        return False


animated_gif_re = re.compile(r'\.gif\[1\]', re.I | re.M)


def _identify_is_animated(image_name):
    try:
        args = ['identify', os.path.abspath(os.path.expanduser(image_name))]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        return True if animated_gif_re.search(output) else False
    except (subprocess.CalledProcessError, OSError) as e:
        print "Failed to get output for '%s': %s" % (args, e)


def is_animated(image_name):
    if Image:
        return _PIL_is_animated(image_name)
    else:
        return _identify_is_animated(image_name)


class AnimatedGif2Png(BaseImageOptimizer):
    provider = 'git2png'
    priority = 100
    output_format = 'png'
    content_types = ['image/gif']
    command = find_executable_path('convert')
    options = []

    def _build_command(self, *args):
        return [self.command] + self.options + [self.input_name, 'png:%s' % self.output_name]
