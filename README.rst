django-boilerplate - yet another django project layout
******************************************************

Description
***********

django-boilerplate is an attempt to set up a standard convention for Django app
layouts, to assist in writing utilities to deploy such applications. A bit of
convention can go a long way.


Related Projects
================

#. `bueda-django-boilerplate <https://github.com/bueda/django-boilerplate>`_


Acknowledgements
================

directory structure::

    django-boilerplate
    ├── apps
    │   ├── core
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── README.rst
    │   │   ├── static
    │   │   │   ├── core
    │   │   │   │   ├── css
    │   │   │   │   │   ├── core.css
    │   │   │   │   │   └── README.rst
    │   │   │   │   ├── img
    │   │   │   │   │   └── README.rst
    │   │   │   │   ├── js
    │   │   │   │   │   ├── core.js
    │   │   │   │   │   └── README.rst
    │   │   │   │   └── lib
    │   │   ├── templates
    │   │   │   ├── base.html
    │   │   │   └── README.rst
    │   │   └── views.py
    │   ├── __init__.py
    │   └── README.rst
    ├── settings
    │   ├── __init__.py
    │   ├── default.py
    │   ├── dev.py
    │   └── urls.py
    ├── __init__.py
    ├── lib
    │   ├── __init__.py
    │   └── README.rst
    ├── manage.py
    ├── README.rst
    ├── requirements
    │   ├── common.txt
    │   ├── dev.txt
    │   ├── production.txt
    │   └── README.rst
    └── static
        └── README.rst


apps
----

All of your Django "apps" go in this directory. These have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's ``INSTALLED_APPS`` list.

Everything in this directory is added to the ``PYTHONPATH`` when
the ``setup`` function from ``environment.py`` is invoked.

There's one predefined app: ``core``. Every base classes should be placed here.
It's also a place to keep your project-level static files. Here's how you might
to organize it::

  apps/core/static/core/      <== application's css, js, img
  apps/core/static/core/lib/  <== css, js libraries

Why is that?

When ``collectstatic`` commands creates the content of ``static`` folder it just
copy contents of static folders from each app. We decide that the best way
to keep clean, resonable and simple structure, will be keeping all static
dependentcies to ``core`` app.

lib
---

Third party Python packages and/or django-apps. Everything in this directory
is added to the ``PYTHONPATH`` when the ``setup`` function from  ``environment.py``
is invoked.


static
------

This folder is fully auto-generated. You don't even need to create it.
It will be created by ``manage.py collectstatic`` command line tool.


requirements
------------

pip requirements files, optionally one for each app environment. The
``common.txt`` is installed in every case.


settings
--------

Very similar to requirements - settings for each environment. There's also
main ``urls.py`` file.


Files
-----

- environment.py

Introduces ``setup`` function that modifies the ``PYTHONPATH`` to allow importing
from the ``apps`` and ``lib`` directories.


- manage.py

The standard Django ``manage.py``.


Authors
-------

* Kuba Janoszek (kuba.janoszek@gmail.com)
* Leszek Piątek jr (lpiatek@gmail.com)
