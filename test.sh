#!/bin/sh

# make a fodler to run all the tests next to eachother
mkdir .testing

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

echo; echo "$numfailed tests failed"

rm -rf .testing