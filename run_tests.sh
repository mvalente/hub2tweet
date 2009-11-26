#!/bin/bash
# Utility script for Python unittests.  Runs all files ending with "_test.py"
# as unittests.  Return code is not zero if one or more fails.

cd `dirname $0`

find . -type f | grep '_test\.py$' | xargs -t -n 1 python

code=$?

if [ $code -gt 0 ]
then
echo "$code test(s) failed.  See output."
else
echo "All tests passed."
fi

exit $code
