 #!/usr/bin/bash  
exec 3>&1
special_echo () {
    echo "$@" >&3
}
exec &>/dev/null

ZP="_Arcade_missing.zip"
TEMP=/media/fat/scripts/temp
ALT=/media/fat/_Arcade/_alternatives

function installfolder {
rm -r "$ALT/$1" >/dev/null
mv -v "$TEMP/_Arcade/_alternatives/$1" "$ALT" >/dev/null
}

clear
special_echo "Getting missing resources"
mkdir $TEMP
cd $TEMP
rm -r _Arcade >/dev/null
rm $ZP >/dev/null
curl https://raw.githubusercontent.com/funkycochise/Coin-Op/master/$ZP -O -k
unzip $ZP -d $TEMP >/dev/null
rm $ZP
##clean previous Zero Wing entries
find /media/fat/_Arcade/ -maxdepth 1 -name 'Zero Wing*' -exec rm -f {} \;
find /media/fat/_Arcade/ -maxdepth 1 -name 'Out Zone*' -exec rm -f {} \;
mv -v $TEMP/_Arcade/*.mra /media/fat/_Arcade

##special_echo "Installing System16 and Atari Tetris"
rm -r "$ALT/_Tetris" >/dev/null
rm -r "$ALT/_Atari Tetris" >/dev/null
installfolder "_Tetris"
installfolder "_Atari Tetris"

##special_echo "Installing SEGA System1/2"
rm /media/fat/_Arcade/cores/SEGASYS1_*.rbf
mv -v $TEMP/_Arcade/SEGASYS1_*.rbf /media/fat/_Arcade/cores

##special_echo "Installing MVS neogeo "
rm -r "/media/fat/_Arcade/Bang Bang Busters.mra" >/dev/null
mv -v $TEMP/_Arcade/neogeo.zip /media/fat/games/mame >/dev/null
rm -r /media/fat/_Arcade/cores/NeoGeo-MVS_*.rbf >/dev/null
mv -v $TEMP/_Arcade/NeoGeo-MVS_*.rbf /media/fat/_Arcade/cores
rm -r /media/fat/_Console/NeoGeo*.rbf >/dev/null
rm -r "/media/fat/_Arcade/Metal Slug 2t.mra" >/dev/null
mv -v $TEMP/_Console/NeoGeo*.rbf /media/fat/_Console/
rm -r "/media/fat/games/mame/s16mcu_alt.zip" >/dev/null
mv -v "$TEMP/_Arcade/s16mcu_alt.zip" "/media/fat/games/mame"

##special_echo "Installing Sega system 1 and 2"
installfolder "_Choplifter"
installfolder "_Gardia"
installfolder "_My Hero"
installfolder "_Pitfall II"
installfolder "_Rafflesia"
installfolder "_Regulus"
installfolder "_Sega Ninja"
installfolder "_Spatter"
installfolder "_Star Jacker"
installfolder "_SWAT"
installfolder "_TeddyBoy Blues"
installfolder "_Toki no Senshi"
installfolder "_UFO Senshi Youko Chan"
installfolder "_Up'n Down"
installfolder "_Water Match"
installfolder "_Wonder Boy"
installfolder "_Wonder Boy in Monster Land" 

##special_echo "Installing Zero Wing & Outzone"
rm -r "/media/fat/games/zerowing" >/dev/null
rm -r "/media/fat/_Arcade/Out Zone*.mra" >/dev/null
find /media/fat/_Arcade/cores -maxdepth 1 -name 'Zero Wing*.rbf' -exec rm -f {} \;
find /media/fat/_Arcade/cores -maxdepth 1 -name 'zerowing*.rbf' -exec rm -f {} \;
find /media/fat/_Arcade/cores -maxdepth 1 -name 'Zerowing*.rbf' -exec rm -f {} \;
mv -v $TEMP/_Arcade/Zerowing*.rbf /media/fat/_Arcade/cores
installfolder "_Zero Wing"
installfolder "_Out Zone"
installfolder "_Hellfire"

cd /media/fat
rm -r "$TEMP"



