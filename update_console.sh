#!/bin/sh
version=0.09
#
#  Based on MiSTer-unstable-nightlies Updater (c) 2021 by Akuma GPLv2
#
corename="PSX"
oldcorename="PlayStation"
coinop_temp="_coinop_temp"

CONSOLE=/media/fat/_Console/
#saturn=https://cdn.discordapp.com/attachments/859157312531071016/978435271257362522/Saturn.rbf
saturn=https://cdn.discordapp.com/attachments/977961301886242897/983410566913728522/Saturn_20220606.rbf
sgb=https://cdn.discordapp.com/attachments/859157312531071016/978714042237616168/SGB.zip

self="$(readlink -f "$0")"

conf="${self%.*}.ini"
[ -f "$conf" ] && . "$conf"

trap "result" 0 1 3 15

result(){
  case "$?" in
    0) echo -e "last version: Github says, last commit on $gitversion"
       echo -e "core version: ${corefile##*/}\n";;
   99) echo "self: updated self";;
  100) echo "error: cannot reach url";;
  101) echo "error: cannot write to sdcard";;
  102) echo "error: download failed";;
  103) echo "error: checksum failed";;
  104) echo "error: json parsing failed";;
  esac
}

makedir(){ [ -d "$1" ] || { mkdir -p "$1" || exit 101;};}
download(){ wget --no-cache -q "$2" -O "$1" || { rm "$1";exit 102;};}
urlcat(){ wget --no-cache -q "$1" -O - || exit 100;}
checksum(){ md5sum "$1"|grep -q "$2" || { rm "$1";exit 103;};}

selfurl="https://raw.githubusercontent.com/Akuma-Git/misterfpga/main/unstable-update_psx-nightlies.sh"
selfurl_version="$(urlcat "$selfurl"|sed -n 's,^version=,,;2p')"

[ "$selfurl_version" = "$version" ] || {
  tempfile="$(mktemp -u)"; download "$tempfile" "$selfurl"
  mv "$tempfile" "$self";chmod +x "$self";exec "$self"; exit 99
}

coredir="/media/fat/$coinop_temp";makedir "$coredir"
gamesdir="/media/fat/games"
psxdir="$gamesdir/${corename}";makedir "$psxdir"

biosurl="https://raw.githubusercontent.com/archtaurus/RetroPieBIOS/master/BIOS/scph1001.bin"
bioshash="924e392ed05558ffdb115408c263dccf"
biosfile="$psxdir/boot.rom"
[ -f "$biosfile" ] || download "$biosfile" "$biosurl"
[ -n "$bioshash" ] && checksum "$biosfile" "$bioshash"

nightliesurl="https://raw.githubusercontent.com/MiSTer-unstable-nightlies/Unstable_Folder_MiSTer/main/db_unstable_nightlies_folder.json"
nightlies="$(urlcat "$nightliesurl")" || exit 100
export $(echo $nightlies|grep -o "\"_Unstable/${corename}.[^}]*}"|sed 's,^.*{,,;s,},,;s,": ,=,g;s/,/\n/g;s,",,g')
[ -n "$url" -o -n "$hash" ] || exit 104

corefile="$coredir/${url##*/}"
[ -f "$corefile" ] || download "$corefile" "$url"
[ -f "$corefile" ] || checksum "$corefile" "$hash"

[ -d "${gamesdir}/${oldcorename}" ] && {
  echo "NOTICE: renaming directories with new core name:"
  find "/media/fat" -maxdepth 2 -type d -name "$oldcorename" -exec rename -v $oldcorename $corename {} \;
}

rm -r /media/fat/_Console/PSX*.rbf >/dev/null
for file in /media/fat/$coinop_temp/*.rbf; do 
    horo="${file%.*}"
    horo="${file:37:8}"
    #echo "file : $file"
    #echo "horo : $horo"
    horo="PSX_$horo.rbf"
    #echo "mv : /media/fat/$coinop_temp/$horo"
    mv "$file" "/media/fat/$coinop_temp/$horo"
    cp "/media/fat/$coinop_temp/$horo" /media/fat/_Console
done

special_echo () {
    echo "$@" >&3
}
exec &>/dev/null


cd "/media/fat/$coinop_temp"
curl $saturn -O -k
rm -r /media/fat/_Console/Saturn*.rbf >/dev/null
cp /media/fat/$coinop_temp/Saturn*.rbf $CONSOLE
special_echo "PSX"
special_echo "Saturn"
curl $sgb -O -k
unzip /media/fat/$coinop_temp/SGB.zip
rm -r /media/fat/_Console/SGB*.rbf >/dev/null
cp /media/fat/$coinop_temp/SGB*.rbf $CONSOLE
special_echo "SGB"
rm -r /media/fat/$coinop_temp

exit 0
