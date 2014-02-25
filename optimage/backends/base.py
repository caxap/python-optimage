#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import logging
import subprocess
import mimetypes

from ..utils import file_size
from ..filetypes import mime_from_file


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
    inline = True
    command = []
    options = []

    @classmethod
    def can_optimize(cls, input_name, validate=True):
        if validate:
            if not os.path.exist(input_name):
                return False
            mimetype = mime_from_file(input_name)
        else:
            mimetype = mimetypes.guess_type(input_name)
        return mimetype in cls.content_types

    def _output_file_name(self):
        ext = '.' + self.output_format
        if not self.inline:
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
        if not self.inline:
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

    def _maybe_copyfile(self):
        if self.input_size > file_size(self.output_name):
            try:
                shutil.copyfile(self.output_name, self.input_name)
                return True
            except IOError as e:
                logger.error("Failed to copy optimized file '%s' (%s)" %
                             (e.filename, e.strerror))
        return False

    def optimize(self, input_name):
        self.optimized = False

        if not self.can_optimize(input_name):
            return self.optimized

        self.input_name = input_name
        self.input_size = file_size(self.input_name)
        self.output_name = self._output_file_name()

        if self._execute_command():
            self.optimized = self._maybe_copyfile()

        self._cleanup()

        return self.optimized

    def _cleanup(self):
        if self.output_name:
            try:
                os.remove(self.output_name)
            except OSError:
                pass
