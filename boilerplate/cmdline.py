# -*- coding: utf-8 -*-
import re
import sys
import optparse
import os
import os.path as ospath
from boilerplate import template, conf

from . import shell, importlib


def output(msg, new_line=1):
    sys.stdout.write("%s" % msg)
    if new_line:
        sys.stdout.write("\n" * new_line)


def cmdname(cmd_class):
    return getattr(cmd_class, 'name', cmd_class.__name__.lower())


register = []


class Command(object):
    def output(self, msg, new_line=1):
        output(msg, new_line)

    def validate_args(self, parser, argv):
        return optparse.OptionParser()

    def handle(self, args, opts):
        pass


class CommandsList(Command):
    name = "cmdlist"
    help = "prints list of available commands"

    def handle(self, args, opts):
        self.output("List of available commands:")
        for cmd_class in register:
            self.output("   %10s - %s" % (
                cmdname(cmd_class),
                cmd_class.help,
            ))
register.append(CommandsList)


class List(Command):
    help = "shows list of available templates"

    def handle(self, args, opts):
        for dirname in os.listdir(conf.templates):
            dirpath = ospath.join(conf.templates, dirname)
            if ospath.isdir(dirpath):
                self.output("   %s" % dirname)
register.append(List)


class Clean(Command):
    help = 'removes all *.pyc *~ files recursively from current directory'

    def handle(self, args, opts):
        shell.rm_maches(os.getcwd(), [
            re.compile(r'.*\.pyc$'),
            re.compile(r'.*\~$'),
        ])
register.append(Clean)


class Create(Command):
    help = "creates new directory from given template"
    usage = "create <template-name> <directory-name>"

    def validate_args(self, parser, argv):
        if len(argv) != 2:
            self.output("Usage: boilerplate %s" % self.usage)
            exit(2)
        return parser

    def get_configuration(self, template_name):
        configuration_module = importlib.import_module('boilerplate.tmpl.%s.config' % template_name)
        return configuration_module.conf

    def handle(self, args, opts):
        template_name = args[0]
        destination_name = args[1]

        current_dir = os.getcwd()
        template_dir = ospath.join(conf.templates, template_name)

        if not ospath.exists(template_dir):
            self.output("No such template directory: %s" % template_dir)
            exit(2)

        config = self.get_configuration(template_name)
        destination_path = ospath.join(current_dir, destination_name)
        template.create(
            template_dir = config.get_template_absolute_path(),
            target = destination_path,
            context = config.get_context(destination_name, template_name=template_name)
        )
        shell.rm_maches(destination_path, [
            re.compile(r'.*\.pyc'),
        ])
register.append(Create)


def top_level_option_parser():
    description = "Available commands: %s" % ', '.join([cmdname(cmd) for cmd in register])
    parser = optparse.OptionParser(
        usage = "usage: %prog <command>",
        description = description,
    )
    return parser


def find_command(name):
    for cmd in register:
        cmd_name = cmdname(cmd)
        if cmd_name == name:
            return cmd
    return None


def handle(argv):
    parser = top_level_option_parser()

    if len(argv) < 1:
        parser.print_help()
        exit(1)

    cmd_class = find_command(argv[0])
    if not cmd_class:
        output("'%s' - no such command" % argv[0], new_line=2)
        parser.print_help()
        exit(1)

    cmd = cmd_class()
    parser = cmd.validate_args(parser, argv[1:])
    opts, args = parser.parse_args(argv[1:])
    return cmd.handle(args, opts)
