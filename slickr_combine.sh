#!/bin/sh

PACKAGE=$1
FRAMESTATS="${PACKAGE##*.}_framestats.txt"
APPDATA="${PACKAGE##*.}_appdata.txt"

if [ "$2" != "" ] ; then
	adb shell am start -a android.intent.action.MAIN -n "$1/$2"
	sleep 1
fi

adb logcat -c

./combine.sh $1 $3 | ./combine.py > $FRAMESTATS 2> $APPDATA

sleep 1

adb shell am force-stop $PACKAGE

echo "./sync_plot.py $FRAMESTATS $APPDATA"