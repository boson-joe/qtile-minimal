#!/bin/sh

# Usage - update_cached_wall.sh TARGET LINK_NAME
#
# This script creates a symbolic link for a TARGET with
# a LINK_NAME. Previous link is deleted, if exists.
#
# boson joe
# https://github.com/boson-joe


echo "\nEntering $0..."

if [ "$#" != 2 ]
then
    echo "Give me two arguments! Exiting..."; exit 1
fi

cached_file="$HOME/.cache/$2"

if [ -L "$cached_file" ]
then
    echo "Unlinking old link..."
    unlink $cached_file
fi

TARGET_BASE_DIR=$(dirname $1)
TARGET_BASE_NAME=$(basename $1)
TARGET_PATH="$TARGET_BASE_DIR/$TARGET_BASE_NAME"
REAL_PATH=$(realpath $TARGET_PATH)

exit_code=0
ln -s $REAL_PATH $cached_file

if [ "$?" = "0" ]
then
    echo "Symbolic link created - $2."
else 
    echo "Error occurred while creating a symbolic link!"
    exit_code=2
fi

exit $exit_code
