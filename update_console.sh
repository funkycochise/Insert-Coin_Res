﻿#!/bin/bash
clear

exec 3>&1
special_echo () {
    echo "$@" >&3
}
exec &>/dev/null


coinop_temp="_coinop_temp"
CONSOLE=/media/fat/_Console/
console_url=https://raw.githubusercontent.com/funkycochise/Coin-Op/main/
console_zip=console.zip
saturn=https://cdn.discordapp.com/attachments/977961301886242897/983410566913728522/Saturn_20220606.rbf
sgb=https://cdn.discordapp.com/attachments/859157312531071016/978714042237616168/SGB.zip


special_echo "Updating Console cores..."
mkdir "/media/fat/$coinop_temp"
cd "/media/fat/$coinop_temp"
curl https://raw.githubusercontent.com/funkycochise/Coin-Op/main/console.zip -O -k >/dev/null
if test -f "/media/fat/$coinop_temp/console.zip"; then
   unzip $console_zip >/dev/null
   rm -r $console_zip >/dev/null
   special_echo "PSX"
   rm -r /media/fat/_Console/PSX*.rbf >/dev/null
   cp /media/fat/$coinop_temp/PSX*.rbf $CONSOLE
   special_echo "Saturn"
   rm -r /media/fat/_Console/Saturn*.rbf >/dev/null
   cp /media/fat/$coinop_temp/Saturn*.rbf $CONSOLE
   special_echo "S32X"
   rm -r /media/fat/_Console/S32X*.rbf >/dev/null
   cp /media/fat/$coinop_temp/S32X*.rbf $CONSOLE
   special_echo "SGB"
   rm -r /media/fat/_Console/SGB*.rbf >/dev/null
   cp /media/fat/$coinop_temp/SGB*.rbf $CONSOLE
   rm -r /media/fat/$coinop_temp
fi