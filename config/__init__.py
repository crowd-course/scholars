from __future__ import absolute_import

from configurations import importer
importer.install()

from .local import Local
from .production import Production


