# -*- coding: utf-8 -*-
# this is <project-name>/conf
from os.path import join, dirname, abspath


here = dirname(abspath(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(here, '..', 'dev.db'),
        }
    }
