boilerplate
-----------

ver. 1.2.2 beta


Very simple templating engine for directories & files structures.


Creating project structure is not a thing I'm doing everyday. Nevertheless
when I'm doing it I always feel frustrated that I don't have anything
prepared. Or when I use some third parties templates I'm pissed off when
"all I need to do is clone repo, remove .git directory, clean README..."
and so on. Using such things is hard because all those templates has also
some dynamic parts (like SECRET_KEY in django projects).


How it works?
=============

After installation new ``boil`` command line tool wil be available for you.
All you need to do is:

1) create you template (eq. ``myfancy_template``) with specialy formed ``_$variables$_``
2) setup all variables parts in ``config.py`` file
3) use your template

::

   myfancy_template/                                                      simpleapp/
     |-- config.py                 $> boil myfancy_template simpleapp        |-- __init__.py
     `-- tmpl/                     =================================>        `-- simpleapp.py
           |
           `-- _$project_name$_/
                  |-- __init__.py
                  `-- _$project_name$_.py


Boilerplate simply creates project / app structure on the given template basis.
You can configurate context variables (only variables) which you can use everywhere
in your templates, even for files or directories names.


How to install?
===============

1) Pip::

   $> pip install boilerplate

2) Download and install::

   $> python setup.py install

3) Or directly from github::

   $> pip install -e git+git://github.com/jqb/boilerplate.git#egg=boilerplate


You need to have root privileges to install it in system packages.


By default boilerplate search for templates in ``$HOME/.boilerplate_templates``
so it's enough if you just create that directory and place your templates there.


You can also set up BOILERPLATE_TEMPLATES environ variable to tell boilerplate where it
should search for your custom templates. You can (should?) setup it in your <dot>-file,
eg in .bashrc ::

  export BOILERPLATE_TEMPLATES=$HOME/.custom_templates


You probably would also want to turn on bash completion in your rc-file::

  eval "`boil --bash-completion`"


Usage
=====

Boilerplate comes with "boil" command line. Here's how you might use it.

#) listing existing templates::

   $> boil -l     # show list of all available templates, you can also type "boil --list"


#) creating new project from existing template::

    $> boil <template-name> <project-name>


    ``project_name`` and ``template_name`` variables are always available your
    template context.


#) creating new project template::

    $> cd $BOILERPLATE_TEMPLATES  # just go to your templates directory
    $> boil boil_template my_first_template


    This is what you gonna get::

    $BOILERPLATE_TEMPLATES/my_first_template/
       |-- __init__.py
       |-- config.py    # meta information about template, context variables for template engine
       `-- tmpl/        # template directory
             |
             `-- _$project_name$_/
                   |
                   `-- _$project_name$__readme.txt


#) using your new project template::

    $> boil my_first_template myproject


#) more controll over creation process

   You are allowed to redifine hooks by passing subclass of ``boilerplate.ProjectCreator``
   to the ``boilerplate.Configuration`` objects in your template ``config.py`` file.
   Eg. if you want to change mode of ``manage.py`` in your own django project template,
   you can do it in this way::


       # $BOILERPLATE_TEMPLATES/my_fancy_django_project_template/config.py
       import subprocess
       from boilerplate import Configuration, ProjectCreator as PC


       class ProjectCreator(PC):
           def after_file_create(self, destination_path):
               if destination_path.endswith('manage.py'):
                   subprocess.call(['chmod', '+x', destination_path])


       conf = Configuration(__file__, {
           # put your context variables here, to use them in your project template
       }, creator_class=ProjectCreator)


   Here's a list of available hooks:

   - ``directory_ignored`` - invoked every time when directory with ``dirname``
     from the template was ignored
     :param: dirname

    - ``file_ignored`` - invoked every time when file with ``file_name`` from the
      template was ignored
      :param: file_name

    - ``before_file_create`` - invoked before every file creation. ``destination_file_path``
      param contains full path to new file
      :param: destination_file_path

    - ``create_file`` - invoked for file creation. It acctually has implementation
      that uses builtin simple template language. You can redefine it in order change
      template engine to your favourite one.
      :param: source_path
      :param: dest_path
      :param: context

    - ``after_file_create`` - invoked with full ``destination_file_path`` after every
      file creation.
      :param: destination_file_path

    - ``before_directory_create``
      :param: destination_dir_path

    - ``after_directory_create``
      :param: destination_dir_path

    - ``before_create`` - invoked before creation of the project with ``destination_path``
      param that contains path to the place where ``boil`` command was invoked
      :param: destination_path

    - ``after_create`` - same as ``before_create`` except it is invoked *after* creation.
      :param: destination_path



TODO
====

* docs for all features available via Configuration objects
* make defining BOILERPLATE_TEMPLATES variable optional,
  maybe ``--create-template-dir`` is a good idea.
