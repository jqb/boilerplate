django-boilerplate -- a standard layout for Django apps
*******************************************************

Description
***********

django-boilerplate is an attempt to set up a standard convention for Django app
layouts, to assist in writing utilities to deploy such applications. A bit of
convention can go a long way.


Related Projects
================

#. `bueda-django-boilerplate <https://github.com/bueda/ops>`_


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
    │   │   │   ├── css
    │   │   │   │   ├── core.css
    │   │   │   │   └── README.rst
    │   │   │   ├── img
    │   │   │   │   └── README.rst
    │   │   │   └── js
    │   │   │       ├── core.js
    │   │   │       └── README.rst
    │   │   ├── templates
    │   │   │   ├── base.html
    │   │   │   └── README.rst
    │   │   └── views.py
    │   ├── __init__.py
    │   └── README.rst
    ├── conf
    │   ├── common.py
    │   ├── dev.py
    │   ├── __init__.py
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
    ├── settings.py
    └── static
        └── README.rst


apps
----

All of your Django "apps" go in this directory. These have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.


lib
---

Third party Python packages and/or django-apps. Everything in this directory
is added to the `PYTHONPATH` when the `environment.py` file is imported.


static
------

A subfolder each for CSS, Javascript and images. Third-party files (e.g. the
960.gs CSS or jQuery) go in a `lib/` subfolder to keep your own code
separate.


requirements
------------

pip requirements files, optionally one for each app environment. The
`common.txt` is installed in every case.

Our Fabfile (see below) installs the project's dependencies from these files.
It's an attempt to standardize the location for dependencies like Rails'
`Gemfile`. We also specifically avoid listing the dependencies in the README of
the project, since a list there isn't checked programmatically or ever actually
installed, so it tends to quickly become out of date.


settings
--------

Very similar to requirements - settings for each environment. There's also
main urls.py file.


Files
-----

- environment.py

Modifies the `PYTHONPATH` to allow importing from the `apps/` and `lib/`
directories. This module is imported at the top of `settings.py` to
make sure it runs for both local development (using Django's built-in server)
and in production (run through mod-wsgi, gunicorn, etc.).

- manage.py

The standard Django `manage.py`.

- settings.py

settings loading.


Authors
-------

* Kuba Janoszek (kuba.janoszek@gmail.com)
* Leszek Piątek jr (lpiatek@gmail.com)
