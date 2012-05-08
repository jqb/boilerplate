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
        names, names_with_places = [], []
        for tmpl_place in conf.templates_directories():
            if not ospath.exists(tmpl_place):
                self.stdout.write(
                    "WARNING Directory: %s, does not exists, omiting.\n" % tmpl_place
                )
                continue

            for dirname in os.listdir(tmpl_place):
                dirpath = ospath.join(tmpl_place, dirname)
                if ospath.isdir(dirpath):
                    names.append(dirname)
                    names_with_places.append((tmpl_place, dirname))

        return names, names_with_places

    def get_template_configuration(self, template_place, template_name):
        sys.path.insert(0, template_place)
        configuration_module = importlib.import_module('%s.config' % template_name)
        sys.path.pop(0)
        return configuration_module.conf

    def get_template_place(self, templates_with_places, template_name):
        for place, name in templates_with_places:
            if template_name == name:
                return place

    def handle(self, argv):
        parser = self.parse_cmdline(argv)
        options, args = parser.parse_args(argv)
        templates_list, templates_with_places = self.get_templates_list()

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

        template_place = self.get_template_place(templates_with_places, template_name)
        project_name = args[1]

        return self.handle_project_creation(template_place, template_name, project_name)

    def handle_project_creation(self, template_place, template_name, project_name):
        template_dir = ospath.join(template_place, template_name)
        destination_path = ospath.join(os.getcwd(), project_name)

        if not ospath.exists(template_dir):
            self.stderr.write("No such template directory: %s" % template_dir)
            return 2

        config = self.get_template_configuration(template_place, template_name)
        creator = config.get_creator()

        creator.before_create(config, template_dir, destination_path)
        creator.create(
            template_dir = config.get_template_absolute_path(),
            target = destination_path,
            context = config.get_context(project_name, template_name=template_name)
        )
        create.after_create(config, template_dir, destination_path)
        return 0
