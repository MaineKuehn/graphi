#!/usr/bin/env bash
set -e

LIB_NAME=graphi
DOCS_DIR=docs

cd ${DOCS_DIR}
touch source/api/placeholder
rm source/api/*
python3 $(which sphinx-apidoc) -M -e -o source/api ../${LIB_NAME} --force && \
python3 $(which sphinx-build) -b html -d build/doctrees . build/html/ && \
open build/html/index.html
