#!/bin/sh

# Usage - update_dunst_colors.sh
#
# This script updates dunst colors on the basis of wal colors.sh.
# Should be used to autostart dunst if you want to preserve colors
# after restarting your wm.
#
# NOTE: if no colors.sh is present in $HOME/.cache/wal/,
# then dunst is just started as a background process 
# (if not active already).
#
# The idea of this script is taken from this good lad - 
# https://www.reddit.com/r/bspwm/comments/d08bzz/dunst_pywal/ez9c1wn?utm_source=share&utm_medium=web2x&context=3
#
# boson joe
# https://github.com/boson-joe


echo "\nEntering $0..."

if [ "$#" != 0 ]
then
    echo "Arguments are not required, but whatever...";
fi

if ! [ -x "$(command -v dunst)" ]
then
    echo "dunst in not present on the system! Exiting..."; exit 1
fi

colors_file="$HOME/.cache/wal/colors.sh" 
if ! [ -f "$colors_file" ]
then
    echo "colors.sh is not created with pywal! No colors are set."
    pidof dunst > /dev/null 2>&1 || dunst &
    exit 2
fi
. $colors_file

pidof dunst > /dev/null 2>&1 && killall dunst

dunst     -lf  "${color7}" \
          -lb  "${color0}" \
          -lfr "${color7}" \
          -nf  "${color1}" \
          -nb  "${color5}" \
          -nfr "${color1}" \
          -cf  "${color7}" \
          -cb  "${color1}" \
          -cfr "${color7}" > /dev/null 2>&1 &

echo "dunst colors are updated!"
exit 0
