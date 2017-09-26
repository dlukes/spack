#!/usr/bin/env zsh

# This is a Python wrapper which makes it more convenient to run scripts in the
# context used by Spack, if need be.

dpath=${0:a:h}
export PYTHONPATH=$dpath/lib/spack:$dpath/lib/spack/external:$PYTHONPATH
exec python $@
