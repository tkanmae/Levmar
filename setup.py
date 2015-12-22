#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.extension import Extension
import numpy as np
from numpy.distutils.system_info import get_info

levmar_sources = [
    'levmar-2.6/lm.c',
    'levmar-2.6/Axb.c',
    'levmar-2.6/misc.c',
    'levmar-2.6/lmlec.c',
    'levmar-2.6/lmbc.c',
    'levmar-2.6/lmblec.c',
    'levmar-2.6/lmbleic.c'
]

lapack_opt = get_info('lapack_opt')
lapack_inc = lapack_opt.pop('include_dirs', None)
include_dirs = ['levmar-2.6', np.get_include()]

if lapack_inc:
    include_dirs += lapack_inc

try:
    from Cython.Distutils import build_ext

    # we have cython, cythonize source
    levmar_sources.append('levmar/_levmar.pyx')
    cmdclass = {'build_ext': build_ext}

except ImportError:
    # no cython, assume they can obtain _levmar.c somehow
    levmar_sources.append('levmar/_levmar.c')
    cmdclass = {}

setup(
    name='levmar',
    version='0.2.0',
    license='GNU General Public Licence v2',
    maintainer='Takeshi Kanmae',
    maintainer_email='tkanmae@gmail.com',
    classifiers=[
        'Intentended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programing Language :: Python',
        'Licence :: OSI Approved :: MIT License',
    ],
    install_requires=open('requirements.txt').read().splitlines(),
    packages=[
        'levmar',
        'levmar.tests',
    ],
    ext_modules=[
        Extension(
            'levmar._levmar',
            cmdclass=cmdclass,
            sources=levmar_sources,
            include_dirs=include_dirs,
            **lapack_opt
        ),
    ],
    zip_safe=False,
    test_suite='nose.collector',
)
