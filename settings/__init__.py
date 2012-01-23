import os

def projectpath(*a):
    from os.path import join, abspath
    return join('/'.join(abspath(__file__).split('/')[0:-2]), *a)

# overwriting settings in order
# settings.default, settings.dev (or settings.DJANGO_ENV), settings.local
execfile('%s/default.py' % projectpath('settings'))
dev = os.environ.get('DJANGO_ENV', 'dev')
if os.path.exists('%s/%s.py' % (projectpath('settings'), dev)):
    execfile('%s/%s.py' % (projectpath('settings'), dev))
if os.path.exists('%s/local.py' % projectpath('settings')):
    execfile('%s/local.py' % projectpath('settings'))

# cleanup
del dev, os
