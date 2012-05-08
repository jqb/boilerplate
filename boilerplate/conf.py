# -*- coding: utf-8 -*-
import os
import os.path as ospath

from .env import create_module_path
from .template import ProjectCreator


modulepath = create_module_path(__file__)
default_templates_dir = modulepath('tmpl')


def templates_directories(paths_environ_name='BOILERPLATE_TEMPLATES', paths_sep=':'):
    paths = os.environ.get(paths_environ_name, '').split(paths_sep)
    paths.insert(0, default_templates_dir)
    return filter(lambda x:x, paths)


class Configuration(object):
    creator_class = ProjectCreator
    context = {}
    template_dir_name = "tmpl"

    def __init__(self, config_file, context=None):
        self.config_file = config_file
        self.context = context or self.__class__.context

    def get_context(self, project_name, template_name=None):
        ctx = dict(self.context)
        ctx.update(project_name=project_name, template_name=template_name)
        return ctx

    def get_creator(self):
        return self.creator_class()

    def get_template_absolute_path(self):
        return ospath.join(ospath.dirname(self.config_file), self.template_dir_name)
