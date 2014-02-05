#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.utils.module_loading import import_by_path

from optimage import optimize as _optimize

__all__ = ['optimize', 'OptimageTemporaryFileUploadHandler']


OPTIMAGE_BACKENDS = getattr(settings, 'OPTIMAGE_BACKENDS', None)


def load_backend_classes():
    if OPTIMAGE_BACKENDS:
        return [import_by_path(p) for p in OPTIMAGE_BACKENDS]


def optimize(input_name, content_type=None, backend_classes=None, **kwargs):
    if not backend_classes:
        backend_classes = load_backend_classes()
    return _optimize(input_name, content_type=content_type,
                     backend_classes=backend_classes, **kwargs)


class OptimageTemporaryFileUploadHandler(TemporaryFileUploadHandler):

    def optimize_file(self, file):
        opened = not file.closed
        if opened:
            file.close()

        self._optimize_file(file)

        if opened:
            file.open()
        return file

    def _optimize_file(self, file):
        optimize(file.name, content_type=file.content_type)

    def file_complete(self, file_size):
        file = super(OptimageTemporaryFileUploadHandler, self).file_complete(file_size)
        return self.optimize_file(file)
