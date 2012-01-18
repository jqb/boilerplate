import os

# Settings cunstomizations ##############################
# the module can be cunstomize via DJANGO_ENV environ variable
for env in ['conf.common', os.environ.get('DJANGO_ENV', 'conf.dev')]:
    config_module = __import__(env, globals(), locals(), env)

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)

# cleaninig up
del config_module, setting, env
