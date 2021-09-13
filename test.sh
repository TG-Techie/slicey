#!/bin/sh

# make a fodler to run all the tests next to eachother
rm -r .testing # clean up old tests for this run
mkdir .testing # make a new testing dir

# copy slicey into it to provide top level access for test
cp slicey.py .testing/slicey.py
cp -r tests/. .testing/

# run each example code to test for errors
numfailed=0
for file in .testing/*
do
    echo; echo "testing $file ..."
    python3 $file 
    ret=$?
    if [ $ret -eq 0 ]; then
        echo "test passed"
    else
        echo "... test failed"
        numfailed=$((numfailed+1))
    fi
done


if [ $numfailed -eq 0 ]; then
    rm -rf .testing
    echo; echo "all tests passed"
else
    echo; echo "$numfailed tests failed"
    echo "leaving test files in place (note: editing them won't edit their intial locations)"
fi