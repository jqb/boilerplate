import os
import site
import sys

from django.utils.importlib import import_module
from django.core.management import setup_environ


def setup(root=None, settings_module_name=None):
    """
    Simple setup snippet that makes easy to create
    fast sandbox to try new things.

    :param root: the root of your project
    :param settings_module_name: name of settings module eg:
         "project.setting"

    Usage:
    >>> from lib import env
    >>> env.setup()
    >>> # from now on paths are setup, and django is configured
    >>> # you can use it in separate "sandbox" script just to check
    >>> # things really quick
    """

    root = root or os.path.dirname(os.path.abspath(__file__))
    path = lambda *a: os.path.join(root, *a)
    settings_module_name = settings_module_name or 'settings'

    # 1) try to import module
    settings = import_module(settings_module_name)

    # 2) setup pythonpath
    if os.path.exists(path('lib')):
        site.addsitedir(path('lib'))

    # 2) cofigure django
    setup_environ(settings)
