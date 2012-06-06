# -*- coding: utf-8 -*-
import os
import errno
import shutil
import os.path as ospath


def mkdir_p(*path):
    try:
        os.makedirs(ospath.join(*path))
    except OSError, exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def mkdir(*path):
    os.makedirs(ospath.join(*path))


def rm_maches(path, patterns=None):
    patterns = patterns or []

    def match_to_remove(name):
        for p in patterns:
            if p.match(name):
                return True
        return False

    for dirname, dirlist, filelist in os.walk(path):
        for f in filelist:
            apath = ospath.join(dirname, f)
            if match_to_remove(apath):
                os.remove(apath)
