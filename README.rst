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

Directory Structure::

    django-layout/
        apps/
	    base/             # base template's, js & css libs as an standard django-app? Why not! :)
	        templates/    # base.html, other "base" templates, some template overrides
		    base.html
		    404.html
	    	    500.html
		static/
		    lib/      # only project-wide js & css libs
 		    images/

            core/             # there always should be "core" app; base classes api's etc.
                models.py
                views.py
                forms.py
		static/       # very basic project things, common for other apps
		    core/
		        js/
			    core.js
			css/
			    core.css
        lib/
        static/               # auto-generated, nothings really here
        requirements/
            common.txt
            dev.txt
            production.txt
	conf/
	    urls.py
	    dev.py
	    production.py
        environment.py    # useful for loading the env just for just-simple-and-fast-check script
        manage.py
        settings.py       # just loads `conf` properly


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
