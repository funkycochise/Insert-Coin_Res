#!/bin/bash

ZP="coinop.zip"
clear

function fileExist()
{
   #echo "$2"
   local  myresult='false'
   if test -f "$2"; then
      myresult='true'
   fi
    local  __resultvar=$1
    #local  myresult='some value'
    eval $__resultvar="'$myresult'"
}
                              
cd /media/fat/scripts
rm -r coinop 2> /dev/null
rm $ZP  2> /dev/null

curl -s https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip -qq $ZP -d /media/fat/scripts/ 

rm $ZP

cd /media/fat/scripts/coinop
sh ./_run.sh

ZIP="/media/fat/Scripts/#pedro/neogeo.zip"
#echo "zip : $ZIP"
fileExist result "/media/fat/Scripts/#pedro/neogeo.zip"
fileExist result "$ZIP"
if [ "$result" = "true" ]; then
   #echo "copying $ZIP to games/mame"
   cp $ZIP /media/fat/games/mame 
fi

cd /media/fat
MF=MiSTer

echo "Installing custom Main"
if [ -d "/media/fat/Mister_" ]; then
   rm /media/fat/Mister_
fi
#echo "Renaming current main mister."
cp /media/fat/Mister /media/fat/Mister_
rm /media/fat/Mister

#echo "Downloading latest main mister."
curl https://raw.githubusercontent.com/funkycochise/Main_MiSTer/master/releases/$MF -O -k
rm /media/fat/Mister_

reboot
