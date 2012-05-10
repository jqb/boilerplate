# -*- coding: utf-8 -*-
"""
Very siple file templating system. Allows to setup
variables and callable variables inside project and apps
templates files.

It procesess line of code, search for the variable name
inside ``_$`` & ``$_`` parentheses. You need to pass
variable via context dictionary to complete processing.

Module also contains function that's able to process
template directory and create project folder.

Usage:
   >>> from boilerplate.template import process_line
   >>> print process_line("def _$function_name$_(*args, **kwargs):\n", {
   >>>     'function_name': 'the_function',
   >>> })
   >>> def the_function(*args, **kwargs):
   >>>
"""
import re
import os
import sys
import os.path as ospath

from . import shell, importlib
from .env import create_module_path


VAR_START = '_$'
VAR_END = '$_'
VAR_RE = re.compile('(%s.*?%s)' % (
    re.escape(VAR_START), re.escape(VAR_END)
))


def resolve(text, context, var_re=VAR_RE):
    if not var_re.match(text):
        return text

    var_name = text.strip().strip(VAR_START).strip(VAR_END).strip()
    val = context[var_name]
    try:
        return val()
    except TypeError:
        return val


def process_line(line, context, var_re=VAR_RE):
    if not var_re.findall(line):
        return line

    return "".join([
        resolve(part, context, var_re=var_re) for part in var_re.split(line)
    ])


class ProjectCreator(object):
    def should_be_ignored(self, path):
        if path.endswith("pyc"):
            return True

        splited = path.split(ospath.sep)
        return ".git" in splited

    def create(self, template_dir=None, target=None, context=None):
        context = context or {}

        template_dir = ospath.abspath(template_dir)
        target = ospath.abspath(target)

        for dirname, dirlist, filelist in os.walk(template_dir):
            if self.should_be_ignored(dirname):
                continue

            dpath = dirname.replace(template_dir, target)
            path = process_line(dpath, context)

            shell.mkdir_p(path)
            for fname in filelist:
                dest_fname = process_line(fname, context)
                source = open(ospath.join(dirname, fname), "r")
                dest = open(ospath.join(path, dest_fname), "w")
                for line in source.xreadlines():
                    dest.write(process_line(line, context))
                dest.close()
                source.close()

    # HOOKS
    def before_create(self, destination_path):
        pass

    def after_create(self, destination_path):
        shell.rm_maches(destination_path, [
            re.compile(r'.*\.pyc'),
        ])
    # END OF HOOKS


class Template(object):
    """
    Class that represents template directory. It has:
    - ``place`` where it is eg. /home/user/.boilerplate_templates/
    - ``name`` of the template

    Template directory should have following structure:

    ::

        <template-name>/
            |-- __init__.py  # this make possible to tread <template-name> as python module
            |-- config.py    # configuration with ``conf`` variable
            `-- tmpl/        # the template contents

    """
    def __init__(self, place=None, name=None):
        self.name = name
        self.place = place

    def exists(self):
        return ospath.exists(self.get_full_path())

    def get_full_path(self):
        return ospath.join(self.place, self.name)

    def get_configuration(self):
        sys.path.insert(0, self.place)
        configuration_module = importlib.import_module('%s.config' % self.name)
        sys.path.pop(0)
        return configuration_module.conf

    def create(self, destination_path, project_name):
        config = self.get_configuration()
        creator = config.get_creator()

        creator.before_create(destination_path)
        creator.create(
            template_dir = config.get_template_absolute_path(),
            target = destination_path,
            context = config.get_context(project_name, template_name=self.name)
        )
        creator.after_create(destination_path)


class TemplateList(list):
    def get_item_with(self, name=None):
        for tmpl in self:
            if tmpl.name == name:
                return tmpl
        return None

    def has_item_with(self, name=None):
        return self.get_item_with(name=name) is not None
