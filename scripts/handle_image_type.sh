#!/bin/sh

# Usage - handle_image_type.sh FILE_NAME DESIRED_FORMAT
#
# This is a helper script to convert an image
# to another format (if needed) using imagemagick.
#
# boson joe
# https://github.com/boson-joe


echo "\nEntering $0..."

if [ "$#" != 2 ]
then
    echo "$0 - Give me two arguments! Exiting..."; exit 1
fi

exit_code=5

desired_t_U=$(echo $2 | tr '[:lower:]' '[:upper:]')
desired_t_l=$(echo $2 | tr '[:upper:]' '[:lower:]')
echo "Desired file type is $desired_t_l."

# Caution! Nasty nested conditionals follow!"
FILE_TYPE=$(file "$1" | grep "$desired_t_U image data")
if [ -z "$FILE_TYPE" ] 
then
    echo "File is not of desired type!"
    
    if ! [ -x "$(command -v mogrify)" ]
    then
        echo "mogrify is not present on the system! Exiting..."; exit 1
    fi

    read -p "Convert? [y\n]:" answer

    case $answer in
        [yY])   mogrify -format $desired_t_l $1 > /dev/null 2>&1
                if [ "$?" != "0" ]
                then
                    echo "Cannot convert file using provided arguments!"
                    exit_code=3
                else
                    echo "File converted!"
                    read -p "Delete the original? [y\n]:" answer
                    case $answer in
                        [yY])   echo "Deleting original file..."
                                rm $1 
                                ;;
                        *   )   echo "No deletion."
                                ;;
                    esac
                    exit_code=0
                fi
                ;;
                
        *   )   echo "Ok, no conversion."      
                exit_code=2 
                ;;
    esac
else
    echo "File type matches the desired one."
    exit_code=0
fi

exit $exit_code
