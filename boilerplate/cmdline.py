# -*- coding: utf-8 -*-
import re
import sys
import optparse
import os
import os.path as ospath

from . import shell, importlib, template, conf, VERSION


def handle(argv):
    handler = Handler()
    return handler.handle(argv)


class HandlerException(Exception):
    pass


completion = dict(
    bash = """
# boilerplate bash completion start
_boilerplate_completion()
{
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   BOILERPLATE_AUTO_COMPLETE=1 $1 ) )
}
complete -o default -F _boilerplate_completion boil
# boilerplate bash completion end
""",
)


class OptionParser(optparse.OptionParser):
    def get_matches(self, comp_word):
        """
        Returns list of options that mathes given ``comp_word``
        """
        result = []
        for opt in self.option_list:
            for opt_str in opt._short_opts + opt._long_opts:
                if opt_str.startswith(comp_word):
                    result.append(opt_str)
        return result


class Handler(object):
    completion = completion

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def parse_cmdline(self, argv):
        parser = OptionParser(
            usage = "usage: %prog <template-name> <project-name>",
            description = "Project structure generation tool",
        )
        parser.add_option("-l", "--list", action="store_true", dest="list", default=False)
        parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
        parser.add_option("--bash-completion", action="store_true", dest="bash_completion", default=False)
        return parser

    def get_templates_places(self):
        return conf.templates_places()

    def get_templates_list(self):
        result = template.TemplateList()

        for tmpl_place in self.get_templates_places():
            if not ospath.exists(tmpl_place):
                self.stdout.write(
                    "WARNING Directory: %s, does not exists, omiting.\n" % tmpl_place
                )
                continue

            for dirname in os.listdir(tmpl_place):
                dirpath = ospath.join(tmpl_place, dirname)
                if ospath.isdir(dirpath):
                    result.append(template.Template(place=tmpl_place, name=dirname))

        return result

    # XXX: move it to other ``Completer`` class or sth like this
    # COMPLETION METHODS
    def completion_request(self):
        return os.environ.get('BOILERPLATE_AUTO_COMPLETE') == '1'

    def can_do_completion(self):
        return len(self.get_complete_words()) <= 1

    def get_complete_words(self):
        return os.environ.get('COMP_WORDS', '').split(" ")[1:]

    def concat(self, words, delimiter=' '):
        return delimiter.join(words)

    def handle_completion(self, parser):
        if self.can_do_completion():
            first = self.get_complete_words()[0]
            self.stdout.write(self.concat([
                t.name
                for t in self.get_templates_list()
                if t.name.startswith(first)
            ]))
            if first.startswith('-'):
                self.stdout.write(self.concat(
                    parser.get_matches(first)
                ))
            self.stdout.write("")
    # END OF COMPLETION METHODS

    def handle(self, argv):
        parser = self.parse_cmdline(argv)
        options, args = parser.parse_args(argv)
        templates_list = self.get_templates_list()

        if self.completion_request():
            self.handle_completion(parser)
            return 0

        if options.version:
            self.stdout.write("%s\n" % VERSION)
            return 0

        if options.list:
            for tmpl in templates_list:
                self.stdout.write("%s\n" % tmpl.name)
            return 0

        if options.bash_completion:
            self.stdout.write(self.completion['bash'])
            return 0

        if len(args) == 0:
            self.stderr.write(
                "There's no enough arguments. Exact two args should be passed."
                "\n"
            )
            parser.print_usage(file=self.stderr)
            return 1

        template_name = args[0]

        if len(args) == 1:
            self.stderr.write(
                "Please add project name"
                "\n"
            )
            parser.print_usage(file=self.stderr)
            return 1

        if not templates_list.has_item_with(name=template_name):
            self.stderr.write("No such template: '%s'\n" % template_name)
            self.stderr.write("Following places has been searched:\n")
            for tmpl_dir in self.get_templates_places():
                self.stderr.write("   %s\n" % tmpl_dir)
            return 1

        template = templates_list.get_item_with(name=template_name)
        project_name = args[1]

        if not template.exists():
            self.stderr.write("No such template directory: %s\n" % template.get_full_path())
            return 2

        destination_path = ospath.join(os.getcwd())
        template.create(destination_path, project_name)

        return 0
