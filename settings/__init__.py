import os

def projectpath(*a):
    from os.path import join, dirname, abspath
    return join(join(dirname(abspath(__file__)), '..'), *a)

files_base_names = [
    'default',
    os.environ.get('DJANGO_ENV', 'dev'),
    'local_settings'
]

for base_name in files_base_names:
    filepath = '%s/%s.py' % (projectpath('settings'), base_name)
    if os.path.exists(filepath):
        execfile(filepath)

# cleanup
del base_name, files_base_names, filepath
