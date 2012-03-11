def create_module_path(thefile, *path):
    from os.path import join, dirname, abspath
    root = abspath(join(dirname(abspath(thefile)), *path))
    return lambda *a: join(root, *a)
