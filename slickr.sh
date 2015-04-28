#!/bin/bash

# Specify the package name of the Android app you want to track
# as the first argument.

# Run 4 times
for i in {1..4}
do
    # Swipe 8 times for 270 ms each.
    for i in {1..8}
    do
        adb shell input touchscreen swipe 100 1600 100 0 270
    done
    adb shell dumpsys gfxinfo $1 | ./profile.py
done