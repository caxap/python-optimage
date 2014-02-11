#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import logging
import subprocess

from ..utils import file_size

__all__ = ['BaseImageOptimizer']


OPTIMAGE_TMP_PREFIX = 'optimage-tmp-'

logger = logging.getLogger('optimage')


class BaseImageOptimizer(object):

    provider = None
    priority = 0
    output_format = None
    # Supported input content types, for now it should correspond with output_format
    content_types = []
    # Should be true for providers that don't support inline optimisation
    output_temp_file = False
    command = []
    options = []

    def __init__(self, input_name):
        self.input_name = input_name

    def _output_file_name(self):
        ext = '.' + self.output_format
        if self.output_temp_file:
            output = tempfile.NamedTemporaryFile(prefix=OPTIMAGE_TMP_PREFIX,
                                                 suffix=ext,
                                                 delete=False)
            output.close()
            return output.name
        else:
            dirname = os.path.dirname(self.input_name)
            basename, _ = os.path.splitext(os.path.basename(self.input_name))
            filename = OPTIMAGE_TMP_PREFIX + basename + ext
            output_name = os.path.join(dirname, filename)
            shutil.copyfile(self.input_name, output_name)
            return output_name

    def _build_command(self, *args):
        cmd = [self.command] + self.options
        if self.output_temp_file:
            return cmd + [self.input_name, self.output_name]
        else:
            return cmd + [self.output_name]

    def _execute_command(self):
        try:
            subprocess.check_call(self._build_command())
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to execute '%s' (exit status %s)" %
                         (e.cmd, e.returncode))
        except IOError as e:
            logger.error("Failed to process file '%s' (%s)" %
                         (e.filename, e.strerror))
        return False

    def optimize(self):
        self.input_size = file_size(self.input_name)
        self.output_name = self._output_file_name()

        if self._execute_command():
            if self.input_size > file_size(self.output_name):
                try:
                    shutil.copyfile(self.output_name, self.input_name)
                except IOError as e:
                    logger.error("Failed to copy optimized file '%s' (%s)" %
                                 (e.filename, e.strerror))
        self._cleanup()

    def _cleanup(self):
        if self.output_name:
            try:
                os.remove(self.output_name)
            except OSError:
                pass
