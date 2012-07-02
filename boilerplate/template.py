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
from .utils import create_module_path


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
    def __init__(self, ignore_files, ignore_directories):
        self.ignore_directories = ignore_directories
        self.ignore_files = ignore_files

    def directory_should_be_ignored(self, path):
        for pattern in self.ignore_directories:
            if pattern.match(path):
                return True
        return False

    def file_should_be_ignored(self, path):
        for pattern in self.ignore_files:
            if pattern.match(path):
                return True
        return False

    def apply_context(self, path, context):
        return process_line(path, context)

    def create_directory(self, dirpath, p=False):
        if p:
            shell.mkdir_p(dirpath)
        else:
            shell.mkdir(dirpath)

    def create(self, template_dir=None, target=None, context=None):
        context = context or {}

        template_dir = ospath.abspath(template_dir)
        target = ospath.abspath(target)

        for dirname, dirlist, filelist in os.walk(template_dir):
            if self.directory_should_be_ignored(dirname):
                self.directory_ignored(dirname)
                continue

            destination_dir_path = dirname.replace(template_dir, target)
            destination_dir_path = self.apply_context(destination_dir_path, context)

            if destination_dir_path != target:
                self.before_directory_create(destination_dir_path)
                self.create_directory(destination_dir_path)
                self.after_directory_create(destination_dir_path)

            for fname in filelist:
                if self.file_should_be_ignored(fname):
                    self.file_ignored(fname)
                    continue

                destination_file_name = self.apply_context(fname, context)
                destination_file_path = ospath.join(
                    destination_dir_path,
                    destination_file_name
                )
                template_file_path = ospath.join(dirname, fname)

                self.before_file_create(destination_file_path)
                self.create_file(template_file_path, destination_file_path, context)
                self.after_file_create(destination_file_path)

    # HOOKS
    def directory_ignored(self, dirname):
        print "DIRECTORY IGNORED:", dirname

    def file_ignored(self, dirname):
        pass

    def before_file_create(self, destination_file_path):
        pass

    def create_file(self, source_path, dest_path, context):
        dest = open(dest_path, "w")
        source = open(source_path, "r")
        for line in source.xreadlines():
            dest.write(self.apply_context(line, context))
        dest.close()
        source.close()

    def after_file_create(self, destination_file_path):
        pass

    def before_directory_create(self, destination_dir_path):
        pass

    def after_directory_create(self, destination_dir_path):
        print "    ", destination_dir_path

    def before_create(self, destination_path):
        pass

    def after_create(self, destination_path):
        pass
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
