import os

def projectpath(*a):
    from os.path import join, abspath
    return join('/'.join(abspath(__file__).split('/')[0:-2]), *a)

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
del base_name, files_base_names
