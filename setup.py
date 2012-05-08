import os
from os.path import join as osjoin
from setuptools import setup, find_packages


def package_data(path):
    data_files = {}
    for dirpath, dirnames, filenames in os.walk(path):
        if filenames:
            data_files[dirpath] = [f for f in filenames]
    return data_files


setup(
    name='boilerplate',
    version='0.8',
    description='boilerplate tool for painless project layout templating',
    author='Kuba Janoszek & Leszek Piatek',
    author_email='kuba.janoszek@gmail.com, lpiatek@gmail.com',
    include_package_data=True,
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
