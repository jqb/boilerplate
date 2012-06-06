import os

def create_projectpath(thefile):
    from os.path import join, dirname, abspath
    root = abspath(join(dirname(abspath(thefile)), '..'))
    return lambda *a: join(root, *a)

# "Temporary globals" that migth be useful
# It can be used in each settings file as builtin
projectpath = create_projectpath(__file__)

# sequence of settings module to read
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
del base_name, files_base_names, filepath, projectpath, create_projectpath
