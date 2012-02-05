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
    >>> import environment
    >>> environment.setup()
    >>> # from now on paths are setup, and django is configured
    >>> # you can use it in separate "sandbox" script just to check
    >>> # things really quick
    """
    root = root or os.path.dirname(os.path.abspath(__file__))
    settings_module_name = settings_module_name or 'settings'

    path = lambda *a: os.path.join(root, *a)

    # 1) try to import module
    settings = import_module(settings_module_name)

    # 2) setup pythonpath
    prev_sys_path = list(sys.path)
    site.addsitedir(path('apps'))
    if os.path.exists(path('lib')):
        for directory in os.listdir(path('lib')):
            full_path = path('lib/%s' % directory)
            if os.path.isdir(full_path):
                site.addsitedir(full_path)

    # Move the new items to the front of sys.path. (via virtualenv)
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)

    sys.path[:0] = new_sys_path

    # 3) cofigure django
    setup_environ(settings)
