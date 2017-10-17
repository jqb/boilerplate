# -*- coding: utf-8 -*-
import os
from os.path import join as osjoin
from setuptools import setup, find_packages

import boilerplate


def package_data(path):
    data_files = {}
    for dirpath, dirnames, filenames in os.walk(path):
        if filenames:
            data_files[dirpath] = [f for f in filenames]
    return data_files


setup(
    name='boilerplate',
    version=boilerplate.VERSION,
    description='Easy to use tool for painless project layout templating',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    include_package_data=True,
    url='https://github.com/jqb/boilerplate/tree/ver-%s' % boilerplate.VERSION,
    packages=find_packages(),
    package_data=package_data(osjoin("boilerplate", "tmpl")),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    scripts=['bin/boil'],
    zip_safe=False,
)


# python setup.py build sdist bdist_wheel upload
