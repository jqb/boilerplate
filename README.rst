boilerplate
-----------

ver. 1.1 beta


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
in your templates, even in files or directories structures.


How to install?
===============

1) Pip::

   $> pip install boilerplate

2) Download and install::

   $> python setup.py install

3) Or directly from github::

   $> pip install -e git+git://github.com/jqb/boilerplate.git#egg=boilerplate


You need to have root privileges to install it in system packages.


Set up BOILERPLATE_TEMPLATES environ variable to tell boilerplate where it
should search for your custom templates. It should be setup in your <dot>-file,
eg in your .bashrc ::

  export BOILERPLATE_TEMPLATES=$HOME/.boilerplate_temlplates


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

    $> cd $BOILERPLATE_TEMPLATES
    $> boil boil_template my_first_template


This is what you gonna get::

    $BOILERPLATE_TEMPLATES/my_first_template/
       |-- __init__.py
       |-- config.py    # meta information about template, context variables for template engine
       `-- tmpl/        # template directory, name "tmpl" will be replaced with "project_name"
             |
             `-- my_first_template/
                   |
                   `-- my_first_template_readme.txt


#) using your new project template::

    $> boil my_first_template myproject


TODO
====

* docs for all features available via Configuration objects
* make defining BOILERPLATE_TEMPLATES variable optional,
  maybe ``--create-template-dir`` is a good idea.
  Default place for BOILERPLATE_TEMPLATES should be ``$HOME/.boilerplate_templates``
  on posix and ``$HOME/BoilerplateTemplates`` on windows/nt
