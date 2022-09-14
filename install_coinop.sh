#!/bin/bash

clear
launchdir=$(pwd)
#echo "launchdir : $launchdir"

ZP="coinop.zip"

cd /media/fat/scripts
rm -r coinop 2> /dev/null
rm $ZP  2> /dev/null

curl -s https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip -qq $ZP -d /media/fat/scripts/ 

rm $ZP

#echo "launchdir : $launchdir"
cd /media/fat/scripts/coinop
sh ./_run.sh $launchdir

rm -r /media/fat/Scripts/coinop >/dev/null

if test -f "$launchdir/update_main_mister.sh"; then
   sh $launchdir/update_main_mister.sh >/dev/null
fi


