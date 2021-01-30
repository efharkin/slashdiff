#!/bin/sh
# Simple install for slashdiff.

# Make slashdiff executable and link it into /usr/local/bin
chmod a+x ./src/slashdiff
ln -s $PWD/src/slashdiff /usr/local/bin
