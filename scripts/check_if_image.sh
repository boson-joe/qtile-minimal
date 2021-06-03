#!/bin/sh

# Usage - check_if_image.sh FILE_NAME
#
# This script uses imagemagick to check if
# the argument provided is an image.
#
# boson joe
# https://github.com/boson-joe


echo "\nEntering $0..."

if [ "$#" != 1 ]
then
    echo "Give me one argument! Exiting..."; exit 1
fi

if ! [ -f "$1" ]
then
    echo "Provided argument is not an existing file! Exiting..."; exit 1
fi

identify $1 > /dev/null 2>&1
if [ "$?" != "0" ]
then
    echo "Provided file is (with high probability) not an image!"
    exit 2
fi

echo "File is indeed an image."
exit 0
