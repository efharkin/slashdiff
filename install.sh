#!/bin/sh
# Simple install for latexdiff.

# Make texdiff executable and link it into /usr/local/bin
chmod a+x ./src/latexdiff
ln -s $PWD/src/latexdiff /usr/local/bin
