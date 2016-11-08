#!/bin/bash
LEVMAR_LAPACK=openblas LEVMAR_BLAS="" ${PYTHON} setup.py build
${PYTHON} setup.py install --single-version-externally-managed --record record.txt
