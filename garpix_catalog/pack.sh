#!/bin/bash

CURRENT_PATH=`dirname "$0"`
CURRENT_PATH=`realpath "$CURRENT_PATH"`
MODULE_NAME=`basename $CURRENT_PATH`

echo "Packing module: $MODULE_NAME"

TEMP_PATH="$CURRENT_PATH/../../tmp/"
TEMP_PATH=`realpath $TEMP_PATH`
VENDOR_PATH="$CURRENT_PATH/../../vendor/"
VENDOR_PATH=`realpath $VENDOR_PATH`

mkdir -p "$TEMP_PATH/$MODULE_NAME"
cp -R "$CURRENT_PATH" "$TEMP_PATH/"
cp "$CURRENT_PATH/setup.py" "$TEMP_PATH/"
cp "$CURRENT_PATH/MANIFEST.in" "$TEMP_PATH/"
rm "$TEMP_PATH/$MODULE_NAME/setup.py"

cd "$TEMP_PATH" && python setup.py sdist --dist-dir="$VENDOR_PATH"

rm -rf "$TEMP_PATH"
rm -rf "./$MODULE_NAME.egg-info"

echo "Finished: $VENDOR_PATH/$MODULE_NAME"
