#!/bin/sh

PID=$(adb shell pidof $1)

if [ "$2" = "" ] ; then
    TWO="-"
else
    TWO=$2
fi

if [ "$3" = "" ] ; then
    THREE="-"
else
    THREE=$3
fi

./slickr.sh $1 $TWO $THREE "cat" > temp.txt

adb shell echo \$EPOCHREALTIME

echo "--------- beginning of data" # needed because of grep
adb logcat -d | grep -e "$PID\s[0-9]\{5\}\sW\sart" -e "$PID\s[0-9]\{5\}\s[A-Z]\sPerf"

echo "$(<temp.txt)"

rm temp.txt