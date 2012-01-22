import os
from extrabuiltins import extrabuiltins

def projectpath(*a):
    from os.path import join, dirname, abspath
    return join(join(dirname(abspath(__file__)), '..'), *a)

with extrabuiltins({'projectpath': projectpath}):
    configuration_files = [
        'settings.default',
        os.environ.get('DJANGO_ENV', 'settings.dev'),
        'settings.local_settings',
    ]
    loaded_modules = []
    for env in configuration_files:
        try:
            config_module = __import__(env, globals(), locals(), env)

            for setting in dir(config_module):
                if setting == setting.upper():
                    locals()[setting] = getattr(config_module, setting)
        except ImportError:
             pass
        else:
            loaded_modules.append(env)
    locals()['LOADED_MODULES'] = loaded_modules

    # cleaninig up
    del config_module, setting, env, loaded_modules, projectpath, extrabuiltins, os
