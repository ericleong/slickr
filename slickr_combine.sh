#!/bin/sh

PACKAGE=$1

if [ "$4" == "" ] ; then
	NAME="${PACKAGE##*.}"
else
	NAME="$4"
fi

FRAMESTATS="${NAME}_framestats.txt"
APPDATA="${NAME}_appdata.txt"
DATA="${NAME}_data.txt"

adb logcat -c

./combine.sh $1 $3 | tee $DATA | ./combine.py > $FRAMESTATS 2> $APPDATA

sleep 1

echo "./sync_plot.py $FRAMESTATS $APPDATA"