boilerplate
-----------

Very simple templating engine for directories & files structures.


UNDER DEVELOPMENT


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


benefits
--------

1) templating is really simple. Uses ONLY VARIABLES within "_$" and "$_".
   It can be use for files & directory names as well as for files contents.

2) it's easy. There's an buildin template for ease template creation::

   $ boil boil_template djangoapp_template
   $ # ... edit my new fancy djangoapp_template template
   $ # ... copy djangoapp_template somewhere where BOILERPLATE_TEMPLATES points
   $ # ... and now you can use it:
   $ boil djangoapp_template pools


Install
-------

Don't do this yet :)
