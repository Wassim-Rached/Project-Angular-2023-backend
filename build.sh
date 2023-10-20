#!/usr/bin/env bash

set -o errexit  # exit on error

make pip-install-prod

make collect-static

make m-prod