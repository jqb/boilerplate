import os

# Settings cunstomizations ##############################
# the module can be cunstomize via DJANGO_ENV environ variableGGCC
for env in ['conf.common', os.environ.get('DJANGO_ENV', 'conf.dev')]:
    config_module = __import__('%s' % env, globals(), locals(), '%s' % env)

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)

# cleaninig up
del config_module, setting, env
