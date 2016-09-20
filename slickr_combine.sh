#!/bin/sh

PACKAGE=$1
FRAMESTATS="${PACKAGE##*.}_framestats.txt"
APPDATA="${PACKAGE##*.}_appdata.txt"

./combine.sh $1 $2 | ./combine.py > $FRAMESTATS 2> $APPDATA
echo "./sync_plot.py $FRAMESTATS $APPDATA"