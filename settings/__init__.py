import os

def projectpath(*a):
    from os.path import join, abspath
    return join('/'.join(abspath(__file__).split('/')[0:-2]), *a)

# overwriting settings in order
# settings.default, settings.dev (or settings.DJANGO_ENV), settings.local
for s in ['default', os.environ.get('DJANGO_ENV', 'dev'), 'local']:
    if os.path.exists('%s/%s.py' % (projectpath('settings'), s)):
        execfile('%s/%s.py' % (projectpath('settings'), s))

# cleanup
del os
