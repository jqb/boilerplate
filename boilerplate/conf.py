# -*- coding: utf-8 -*-
import re
import os
import os.path as ospath

from .utils import create_module_path, userhome_path, paths_separator
from .template import ProjectCreator
from . import filematchers as matchers


modulepath = create_module_path(__file__)  # boilerplate module path
default_templates_dir = modulepath('tmpl')
default_user_templates_dir_name = ".boilerplate_templates"


def templates_places(paths_environ_name='BOILERPLATE_TEMPLATES',
                     paths_sep=paths_separator,
                     user_templates_dir_name=default_user_templates_dir_name):
    """
    Returns all places in the file system where we should search for templates.
    Default templates in boilerplate module are defined in the boilerplate package
    and are always available. The other places you can define in BOILERPLATE_TEMPLATES
    environment variable.

    For example, if you do not have BOILERPLATE_TEMPLATES defined this is what you might
    get in the command line.

    Default value of BOILERPLATE_TEMPLATES is "$HOME/.boilerplate_templates", so you
    can just create the directory and start to create your own templates.

    ::

        $ boil -l
        boil_template

    "boil_template" is the build in template (which you can use to create other templates).
    Once you defined BOILERPLATE_TEMPLATES as follows, you will be able to use your own
    templates (or third parties).

    ::

        $ mkdir -p /home/user/.boilerplate_templates/
        $ export BOILERPLATE_TEMPLATES=/home/user/.boilerplate_templates/
        $ cd $BOILERPLATE_TEMPLATES
        $ boil boil_template my_fancy_template

    And now you'll be able to use your new shiny "my_fancy_template"

    ::

        $ boil -l
        boil_template
        my_fancy_template

    """
    paths = os.environ.get(
        paths_environ_name,
        userhome_path(user_templates_dir_name)
    ).split(paths_sep)
    paths.insert(0, default_templates_dir)
    return filter(lambda x:x, paths)


class Configuration(object):
    creator_class = ProjectCreator
    context = {}
    template_dir_name = "tmpl"
    ignore_directories = [
        matchers.git_directory,
        matchers.svn_directory,
    ]
    ignore_files = [
        matchers.pyc_files,
    ]

    def __init__(self, config_file, context=None, creator_class=None):
        self.config_file = config_file
        self.context = context or self.__class__.context
        self.creator_class = creator_class or self.__class__.creator_class

    def get_context(self, project_name, template_name=None):
        ctx = dict(self.context)
        ctx.update(project_name=project_name, template_name=template_name)
        return ctx

    def get_creator(self):
        return self.creator_class(self.ignore_files, self.ignore_directories)

    def get_template_absolute_path(self):
        return ospath.join(ospath.dirname(self.config_file), self.template_dir_name)
