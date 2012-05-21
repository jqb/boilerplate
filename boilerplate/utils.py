# -*- coding: utf-8 -*-
import os
from os.path import join, dirname, abspath


def create_module_path(thefile, *path):
    root = abspath(join(dirname(abspath(thefile)), *path))
    return lambda *a: join(root, *a)


def _posix_home(*path):
    return join(os.environ["HOME"], *path)


def _nt_home(*path):
    return join(
        os.environ["HOMEDRIVE"],
        os.environ["HOMEPATH"],
        *path
    )


_systems = {
    'posix': _posix_home,
    'nt': _nt_home,
}


def userhome_path(*path):
    get_home_path = _systems[os.name]
    return get_home_path(path)
