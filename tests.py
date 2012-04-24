# -*- coding: utf-8 -*-
from cStringIO import StringIO
import unittest

from boilerplate import cmdline


class CommandLineHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = cmdline.Handler(
            stdout = StringIO(),
            stderr = StringIO(),
        )

    def test_it_fails_when_no_arguments_or_options_applied(self):
        self.handler.handle([])
        msg = self.handler.stderr.getvalue()
        assert msg.startswith("There's no enough arguments"), "Wrong message | %s" % msg

    def test_it_fails_then_theres_no_enougth_arguments(self):
        template_name = "boil_template"  # standard template, always exists
        args = [template_name]

        self.handler.handle(args)
        msg = self.handler.stderr.getvalue()
        assert msg.startswith("Please add project name"), "Wrong message | %s" % msg

    def test_it_should_have_at_least_one_default_template(self):
        res = self.handler.get_templates_list()
        assert len(res) > 1, "There should be at least one template by default."


if __name__ == '__main__':
    unittest.main()
