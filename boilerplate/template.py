# -*- coding: utf-8 -*-
"""
Very siple file templating system. Allows to setup
variables and callable variables inside project and apps
templates files.

It procesess line of code, search for the variable name
inside ``{{`` & ``}}`` parentheses. You need to pass
variable via context dictionary to complete processing.

Module also contains function that's able to process
template directory and create project folder.

Usage:
   >>> from boilerplate.template import process_line
   >>> print process_line("def {{ function_name }}(*args, **kwargs):\n", {
       'function_name': 'the_function',
   })
   >>> def the_function(*args, **kwargs):
   >>>
"""
import re
import os
import os.path as ospath

from . import shell


var_re = re.compile('(%s.*?%s)' % (
    re.escape('{{'), re.escape('}}')
))

def resolve(text, context):
    if not var_re.match(text):
        return text

    var_name = text.strip().strip('{{').strip('}}').strip()
    val = context[var_name]
    try:
        return val()
    except TypeError:
        return val

def process_line(line, context):
    if not var_re.findall(line):
        return line

    return "".join([
        resolve(part, context) for part in var_re.split(line)
    ])

def should_be_ignored(path):
    if path.endswith("pyc"):
        return True

    splited = path.split(ospath.sep)
    return ".git" in splited

def create(template_dir=None, target=None, context=None):
    context = context or {}

    template_dir = ospath.abspath(template_dir)
    target = ospath.abspath(target)

    for dirname, dirlist, filelist in os.walk(template_dir):
        if should_be_ignored(dirname):
            continue

        path = dirname.replace(template_dir, target)
        shell.mkdir_p(path)
        for fname in filelist:
            source = open(ospath.join(dirname, fname), "r")
            dest = open(ospath.join(path, fname), "w")
            for line in source.xreadlines():
                dest.write(process_line(line, context))
            dest.close()
            source.close()


class Configuration(object):
    context = {}
    template_dir_name = "tmpl"

    def __init__(self, config_file, context=None):
        self.config_file = config_file
        self.context = context or self.__class__.context

    def get_context(self, dirname):
        return self.context

    def get_template_absolute_path(self):
        return ospath.join(ospath.dirname(self.config_file), self.template_dir_name)
