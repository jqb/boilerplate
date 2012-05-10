boilerplate
-----------

ver. 1.0 alpha


Very simple templating engine for directories & files structures.


Creating project structure is not thing I'm doing everyday. Nevertheless
when I'm doing it I always feel frustrated that I don't have anything
prepared. Or when I use some third parties templates I'm pissed off when
"all I need to do is clone repo, remove .git directory, clean README..."
and so on. Using such things is hard because all those templates has also
some dynamic parts (like SECRET_KEY in django project).


How it works?
-------------

::

   myfancy_template/                                                      simpleapp/
     |-- config.py                 $> boil myfancy_template simpleapp        |-- __init__.py
     `-- tmpl/                     =================================>        `-- simpleapp.py
           |-- __init__.py
           `-- _$project_name$_.py


Boilerplate simply creates project / app structure on the given template basis.
You can configurate context variables (only variables) which you can use everywhere
in your templates, even in files or directories structures.


How to install?
---------------

Download and install::

  python setup.py install

or directly from github::

  pip install -e git+git://github.com/jqb/boilerplate.git#egg=boilerplate


.. NOTE::

   You need to have root privilleges to install in system packages.


Set up BOILERPLATE_TEMPLATES environ variable to tell boilerplate where it
should search for your custom templates. It should be setup in your <dot>-file,
eg in your .bashrc ::

  export BOILERPLATE_TEMPLATES=$HOME/.boilerplate_temlplates


Usage
-----

Boilerplate comes with "boil" command line. Here's how you might use it.

#) listing existing templates::

   $> boil -l     # show list of all available templates, you can also type "boil --list"
   boil_template


#) creating new project from existing template::

   $> boil <template-name> <project-name>


.. NOTE ::

    ``project_name`` variable and ``template_name`` are always available your
    template context.


#) creating new project template::

   $> cd $BOILERPLATE_TEMPLATES
   $> boil boil_template my_first_template


This is what you gonna get::

   $BOILERPLATE_TEMPLATES/my_first_template/
       |-- __init__.py
       |-- config.py    # meta information about template, context variables for template engine
       `-- tmpl/        # template directory, name "tmpl" will be replaced with "project_name"
             `-- my_fancy_template_readme.txt


#) using my new project template::

    $> boil my_first_template myproject


TODO
----

  * docs for all features available via Configuration objects
