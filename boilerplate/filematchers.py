# -*- coding: utf-8 -*-
import re
from os import path as ospath


class GitDirectory(object):
    def match(self, path):
        splited = path.split(ospath.sep)
        return ".git" in splited


git_directory = GitDirectory()
pyc_files = re.compile('.*\.pyc$')
