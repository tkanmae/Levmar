#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import pprint
import shutil
import sys
import warnings

from setuptools import setup
from setuptools.extension import Extension

pkg_name = 'levmar'
url = 'https://github.com/bjodah/' + pkg_name
license = 'GNU General Public Licence v2'  # Takeshi Kanmae's wrapper code has the MIT license

levmar_sources = [
    'levmar/levmar-2.6/lm.c',
    'levmar/levmar-2.6/Axb.c',
    'levmar/levmar-2.6/misc.c',
    'levmar/levmar-2.6/lmlec.c',
    'levmar/levmar-2.6/lmbc.c',
    'levmar/levmar-2.6/lmblec.c',
    'levmar/levmar-2.6/lmbleic.c'
]


def _path_under_setup(*args):
    return os.path.join(os.path.dirname(__file__), *args)

release_py_path = _path_under_setup(pkg_name, '_release.py')
config_py_path = _path_under_setup(pkg_name, '_config.py')
env = None  # silence pyflakes, 'env' is actually set on the next line
exec(open(config_py_path).read())
for k, v in list(env.items()):
    env[k] = os.environ.get('%s_%s' % (pkg_name.upper(), k), v)


USE_CYTHON = os.path.exists(_path_under_setup(pkg_name, '_levmar.pyx'))
# Cythonize .pyx file if it exists (not in source distribution)
ext_modules = []

if len(sys.argv) > 1 and '--help' not in sys.argv[1:] and sys.argv[1] not in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    import numpy as np
    ext = '.pyx' if USE_CYTHON else '.c'
    ext_modules = [Extension('%s._levmar' % pkg_name,
                             [os.path.join('levmar', '_levmar' + ext)] + levmar_sources)]
    if USE_CYTHON:
        from Cython.Build import cythonize
        ext_modules = cythonize(ext_modules)
    ext_modules[0].include_dirs = ['levmar/levmar-2.6', np.get_include()]
    if env['LAPACK']:
        ext_modules[0].libraries += [env['LAPACK']]
    if env['BLAS']:
        ext_modules[0].libraries += [env['BLAS']]

_version_env_var = '%s_RELEASE_VERSION' % pkg_name.upper()
RELEASE_VERSION = os.environ.get(_version_env_var, '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
if os.environ.get('CONDA_BUILD', '0') == '1':
    try:
        RELEASE_VERSION = 'v' + open(
            '__conda_version__.txt', 'rt').readline().rstrip()
    except IOError:
        pass


if len(RELEASE_VERSION) > 1:
    if RELEASE_VERSION[0] != 'v':
        raise ValueError("$%s does not start with 'v'" % _version_env_var)
    TAGGED_RELEASE = True
    __version__ = RELEASE_VERSION[1:]
else:  # set `__version__` from _release.py:
    TAGGED_RELEASE = False
    exec(open(release_py_path).read())

classifiers = [
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: MIT License',
]

tests = [
    '%s.tests' % pkg_name,
]

with io.open(_path_under_setup(pkg_name, '__init__.py'), 'rt', encoding='utf-8') as f:
    short_description = f.read().split('"""')[1].split('\n')[1]
if not 10 < len(short_description) < 255:
    warnings.warn("Short description from __init__.py proably not read correctly")
long_descr = io.open(_path_under_setup('README.rst'), encoding='utf-8').read()
if not len(long_descr) > 100:
    warnings.warn("Long description from README.rst probably not read correctly.")
_author, _author_email = open(_path_under_setup('AUTHORS'), 'rt').readline().split('<')
_author_email = _author_email.split('>')[0].strip() if '@' in _author_email else None

setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=short_description,
    long_description=long_descr,
    classifiers=classifiers,
    author=_author.strip(),
    author_email=_author_email,
    maintainer='Björn Dahlgren',
    maintainer_email='bjodah@gmail.com',
    url=url,
    license=license,
    packages=[pkg_name] + tests,
    install_requires=['numpy'] + (['cython'] if USE_CYTHON else []),
    setup_requires=['numpy'] + (['cython'] if USE_CYTHON else []),
    extras_require={'docs': ['Sphinx', 'sphinx_rtd_theme', 'numpydoc']},
    ext_modules=ext_modules,
    zip_safe=False,
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set PYGSLODEIV2_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            open(release_py_path, 'wt').write(
                "__version__ = '{}'\n".format(__version__))
        shutil.move(config_py_path, config_py_path+'__temp__')
        open(config_py_path, 'wt').write("env = {}\n".format(pprint.pformat(env)))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
        shutil.move(config_py_path+'__temp__', config_py_path)
