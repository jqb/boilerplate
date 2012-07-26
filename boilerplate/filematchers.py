# -*- coding: utf-8 -*-
import re
from os import path as ospath


class DirectoryMatcher(object):
    def __init__(self, name):
        self.name = name

    def match(self, path):
        splited = path.split(ospath.sep)
        return self.name in splited


git_directory = DirectoryMatcher(".git")
svn_directory = DirectoryMatcher(".svn")
pyc_files = re.compile('.*\.pyc$')
