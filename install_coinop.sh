#!/bin/bash

ZP="coinop.zip"

cd /media/fat/scripts
rm -r coinop 2> /dev/null
rm $ZP  2> /dev/null

curl -s https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip -qq $ZP -d /media/fat/scripts/ 

rm $ZP

cd /media/fat/scripts/coinop
sh ./_run.sh 