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

# Android Marshmallow features
# http://developer.android.com/preview/testing/performance.html#timing-info
VERSION=$(adb shell getprop ro.build.version.release)
MAJOR_VERSION=$(echo $VERSION | cut -c 1)
MINOR_VERSION=$(echo $VERSION | cut -c 3)
if [ "$1" != "" ] ; then
    # Test if integer, then test if >= 6.0
    if [[ "$MAJOR_VERSION" =~ ^-?[0-9]+$ ]] && [ "$MAJOR_VERSION" -ge "6" ] ; then
        FRAMESTATS="framestats"
    elif [ "$MAJOR_VERSION" == "N" ] ; then # N preview
        FRAMESTATS="framestats"
    fi
fi

# Scroll command differs by version

SWIPE="touchscreen swipe"
DURATION="250"

if [[ "$MAJOR_VERSION" =~ ^-?[0-9]+$ ]] ; then
    if [ "$MAJOR_VERSION" -ge "5" ] ; then
        :
    elif [ "$MAJOR_VERSION" -ge "4" ] && [ "$MINOR_VERSION" -gt "1" ] ; then
        :
    else
    	# Old device
        SWIPE="swipe"
        DURATION=""
    fi
fi

# Empty old data
adb shell dumpsys gfxinfo $1 > /dev/null

# Collect data for $COUNT times
if [ $COUNT -gt "1" ] ; then

    # Swipe three times for 250 ms each.
    # adb shell is a little slow, so when this is finished,
    # about 128 frames (2 seconds at 60 fps) should have passed.
    # Afterwards, dump data and filter for profile data
    adb shell "for i in `seq -s ' ' 1 $COUNT`; do for j in `seq -s ' ' 1 3`; do input $SWIPE 100 $VERTICAL 100 0 $DURATION; done; dumpsys gfxinfo $1 $FRAMESTATS; done;" | ./profile.py
else
    adb shell "for j in `seq -s ' ' 1 3`; do input $SWIPE 100 $VERTICAL 100 0 $DURATION; done; dumpsys gfxinfo $1 $FRAMESTATS;" | ./profile.py
fi
