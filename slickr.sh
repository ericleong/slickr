#!/bin/bash

# Specify the package name of the Android app you want to track
# as the first argument.

# Swipe by 3x the density of the device.
# TODO: account for landscape
VERTICAL=$(expr $(adb shell wm density | grep -o '[0-9]\+') \* 3)

# Run 4 times
for i in {1..${2:-4}}
do
    # Swipe 8 times for 250 ms each.
    # This works out to 2000 ms, which is about the duration of 128 frames at 60 FPS
    for i in {1..8}
    do
        adb shell input touchscreen swipe 100 ${3:-$VERTICAL} 100 0 250
    done
    adb shell dumpsys gfxinfo $1 | ./profile.py
done