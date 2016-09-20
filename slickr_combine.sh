#!/bin/sh

PACKAGE=$1

if [ $4 != "" ] ; then
	NAME="$4"
else
	NAME="${PACKAGE##*.}"
fi

FRAMESTATS="${NAME}_framestats.txt"
APPDATA="${NAME}_appdata.txt"
DATA="${NAME}_data.txt"

# if [ "$2" != "" ] ; then
# 	adb shell am start -a android.intent.action.MAIN -n "$1/$2"
# 	sleep 5
# fi

adb logcat -c

# ./combine.sh $1 $3 | tee $DATA | ./combine.py > $FRAMESTATS 2> $APPDATA
./combine.sh $1 $3 | ./combine.py > $FRAMESTATS 2> $APPDATA

sleep 1

adb shell am force-stop $PACKAGE

echo "./sync_plot.py $FRAMESTATS $APPDATA"