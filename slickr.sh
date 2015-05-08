#!/bin/sh

# Specify the package name of the Android app you want to track
# as the first argument.

# Number of times to run
if [ "$2" = "" ] ; then
    COUNT=4
else
    COUNT=$2
fi

# Vertical pixels to swipe
if [ "$3" = "" ] ; then

    # Try to get density with "wm"
    DENSITY=$(adb shell wm density)

    if [[ $DENSITY == *"wm: not found"* ]] ; then
        # Grab density with "getprop"
        DENSITY=$(adb shell getprop | grep density)
    fi

    # Grab actual density value
    DENSITY=$(echo $DENSITY | grep -o "[0-9]\+")

    VERTICAL=$(expr $DENSITY \* 3)
else
    VERTICAL=$3
fi

for ((i=1; i<=$COUNT; i++))
do
    # Swipe 8 times for 250 ms each.
    # This works out to 2000 ms, which is about the duration of 128 frames at 60 FPS
    for j in {1..8}
    do
        adb shell input touchscreen swipe 100 $VERTICAL 100 0 250
    done
    adb shell dumpsys gfxinfo $1 | ./profile.py
done