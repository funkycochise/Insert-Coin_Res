#!/bin/bash

ZP="coinop.zip"

cd /media/fat/scripts
rm -r coinop >/dev/null
rm $ZP >/dev/null

curl https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip $ZP -d /media/fat/scripts/

rm $ZP

cd /media/fat/scripts/coinop
sh ./_run.sh 