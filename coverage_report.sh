#!/usr/bin/env bash

set -e
coverage run manage.py test
coverage report > coverage.txt
echo "Coverage report generated in coverage.txt"
