#!/usr/bin/env python

import sys
from django.conf import settings


def _get_func(name):
  """
  Import and return the function ``name`` (which includes its module name).
  """

  parts = name.split(".")
  module_name = ".".join(parts[:-1])
  func_name = parts[-1]

  __import__(module_name)
  module = sys.modules[module_name]

  return getattr(module, func_name)


def url_to_html(url):
  for name in settings.EMBED_PROCESSORS:
    func = _get_func(name)
    html = func(url)

    if html is not None:
      return '<div class="embed %s">%s</div>' %\
        (func.__name__, html)

  return url