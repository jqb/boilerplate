import os
import site
import sys

from django.utils.importlib import import_module
from django.core.management import setup_environ


def setup(root=None, settings_module_name=None):
    """
    Simple setup snippet that makes easy to create
    fast sandbox to try new things.

    This script assumes that "environment.py" is your
    project directory (the same place as "manage.py").
    But you can change this behavior using optional params:

    :param root: the root of your project
    :param settings_module_name: name of settings module eg:
         "project.setting"

    Usage:
    >>> import env
    >>> env.setup()
    >>> # from now on paths are setup, and django is configured
    >>> # you can use it in separate "sandbox" script just to check
    >>> # things really quick
    """

    root = root or os.path.dirname(os.path.abspath(__file__))
    settings_module_name = settings_module_name or 'settings'

    # 1) try to import module
    settings = import_module(settings_module_name)

    # 2) cofigure django
    setup_environ(settings)
