#!/bin/sh

# Usage - wal_update.sh FILE_NAME
#
# This script updates wallpaper and colors of some applications
# by calling pywal and some helper scripts.
#
# boson joe
# https://github.com/boson-joe


if [ "$#" != "1" ]
then
    echo "Give me one argument! Exiting..."; exit 1
fi

echo "Argument is $1"
argument=$1
if ! [ -f "$argument" ]
then
    echo "Provided argument is not an existing file! Exiting..."; exit 1
fi

BASE_DIR="$(dirname $0)/"

script_to_call="${BASE_DIR}check_if_image.sh"
if [ -f "$script_to_call" ]
then
    echo "Calling $script_to_call..."
    sh $script_to_call $argument
    if [ "$?" != "0" ]
    then
        exit 2
    fi
else
    "No script for checking type of an argument! Exiting..."; exit 2
fi
echo ""

CORRECT_IMAGE_TYPE=1
file_type=png
script_to_call="${BASE_DIR}handle_image_type.sh"
if [ -f "$script_to_call" ]
then
    echo "Calling $script_to_call..."
    sh $script_to_call $argument "$file_type"
    CORRECT_IMAGE_TYPE=$?
    if [ "$CORRECT_IMAGE_TYPE" = "0" ]
    then
        argument=${argument%.*}.$file_type
    fi
fi
echo ""

if ! [ -x "$(command -v wal)" ]
then
    echo "wal in not present on the system! Exiting..."; exit 1
fi

echo "Calling wal on the provided argument..."
wal -i $argument > /dev/null

script_to_call="${BASE_DIR}update_dunst_colors.sh"
if [ -f $script_to_call ]
then
    echo "Calling $script_to_call..."
    sh $script_to_call
fi
echo ""

script_to_call="${BASE_DIR}update_cached_wall.sh"
if [ -f $script_to_call ]
then
    echo "Calling $script_to_call..."
    sh $script_to_call $argument "current_wallpaper"
fi
echo ""

if [ -f $script_to_call ] && [ "$CORRECT_IMAGE_TYPE" = "0" ]
then
    echo "Calling $script_to_call..."
    sh $script_to_call $argument "current_lock_background"
fi
echo ""
