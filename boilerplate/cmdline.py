# -*- coding: utf-8 -*-
import re
import sys
import optparse
import os
import os.path as ospath

from . import shell, importlib, template, conf


def handle(argv):
    handler = Handler()
    return handler.handle(argv)


class HandlerException(Exception):
    pass


class Handler(object):
    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def parse_cmdline(self, argv):
        parser = optparse.OptionParser(
            usage = "usage: %prog <template-name> <project-name>",
            description = "Project structure generation tool",
        )
        parser.add_option("-l", "--list", action="store_true", dest="list", default=False)
        return parser

    def get_templates_list(self):
        result = []
        for dirname in os.listdir(conf.templates):
            dirpath = ospath.join(conf.templates, dirname)
            if ospath.isdir(dirpath):
                result.append(dirname)
        return result

    def get_configuration(self, template_name):
        configuration_module = importlib.import_module('boilerplate.tmpl.%s.config' % template_name)
        return configuration_module.conf

    def handle(self, argv):
        parser = self.parse_cmdline(argv)
        options, args = parser.parse_args(argv)
        templates_list = self.get_templates_list()

        if options.list:
            for tmpl in templates_list:
                self.stdout.write("%s\n" % tmpl)
            return 0

        if len(args) == 0:
            self.stderr.write(
                "There's no enough arguments. Exact two args should be passed."
                "\n"
            )
            parser.print_usage(file=self.stderr)
            return 1

        template_name = args[0]

        if len(args) == 1 and template_name in templates_list:
            self.stderr.write(
                "Please add project name"
                "\n"
            )
            parser.print_usage(file=self.stderr)
            return 1

        project_name = args[1]

        return self.handle_project_creation(template_name, project_name)


    def handle_project_creation(self, template_name, project_name):
        current_dir = os.getcwd()
        template_dir = ospath.join(conf.templates, template_name)

        if not ospath.exists(template_dir):
            self.stderr.write("No such template directory: %s" % template_dir)
            return 2

        config = self.get_configuration(template_name)
        creator = config.get_creator()

        destination_path = ospath.join(current_dir, project_name)
        creator.create(
            template_dir = config.get_template_absolute_path(),
            target = destination_path,
            context = config.get_context(project_name, template_name=template_name)
        )
        shell.rm_maches(destination_path, [
            re.compile(r'.*\.pyc'),
        ])

        return 0
