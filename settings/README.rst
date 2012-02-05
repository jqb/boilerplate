Settings
--------

Setting loading sequence is defined in ``settings/__init__.py`` file,
in ``filed_base_names`` variable. The predefined sequence is:

* ``settings.default``
* ``settings.<DJANGO_ENV variable>`` if DJANGO_ENV environ variable is defined,
  ``settings.dev`` overwise
* ``local_settings`` - it NOT exists. Tf you want to have your your own
  local settings just create ``local_settings.py`` file and fill it with your
  choices.
