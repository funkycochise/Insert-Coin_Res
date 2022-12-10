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
curl https://raw.githubusercontent.com/funkycochise/Main_MiSTer/master/releases/$MF -O -k -s
if test -f "/media/fat/Mister"; then
   echo "Main Mister installed."
   rm /media/fat/Mister_
else
   echo "Something went wrong while trying to download main Mister."
   echo "Previous Main Mister is restored."
   cp /media/fat/Mister_ /media/fat/Mister
   rm /media/fat/Mister_
fi

echo ""

