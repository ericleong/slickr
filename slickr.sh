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

# Android M features
if [ "$1" != "" ] && [[ "$(adb shell getprop ro.build.version.release)" == "M"* ]] ; then

    # http://developer.android.com/preview/testing/performance.html#timing-info
    FRAMESTATS="framestats"
else
    FRAMESTATS=""
fi

# Empty old data
adb shell dumpsys gfxinfo $1 > /dev/null

# Collect data for $COUNT times

# Swipe three times for 250 ms each.
# adb shell is a little slow, so when this is finished,
# about 128 frames (2 seconds at 60 fps) should have passed.
# Afterwards, dump data and filter for profile data
adb shell "for i in `seq -s ' ' 1 $COUNT`; do for j in `seq -s ' ' 1 3`; do input touchscreen swipe 100 $VERTICAL 100 0 250; done; dumpsys gfxinfo $1 $FRAMESTATS; done;" | ./profile.py