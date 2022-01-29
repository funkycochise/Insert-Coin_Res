#!/bin/bash

ZP="coinop.zip"
clear
                              

cd /media/fat/scripts
rm -r coinop 2> /dev/null
rm $ZP  2> /dev/null

curl -s https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip -qq $ZP -d /media/fat/scripts/ 

rm $ZP

cd /media/fat/scripts/coinop
sh ./_run.sh 

cd /media/fat/Scripts/#pedro
sh ./install_neogeozip.sh
sh ./install_main_mister.sh