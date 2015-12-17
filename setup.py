#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.extension import Extension
import numpy as np
from numpy.distutils.system_info import get_info

levmar_sources = [
    'levmar/_levmar.c',
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
            sources=levmar_sources,
            include_dirs=['levmar-2.6', np.get_include()] + lapack_inc,
            **lapack_opt
        ),
    ],
    zip_safe=False,
    test_suite='nose.collector',
)
