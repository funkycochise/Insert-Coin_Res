# redirect stdout/stderr to a file
#exec >run.txt 2>&1

launchdir=$1
#special_echo "launchdir $launchdir"

echo "Cleaning console mgl"

#gameboy color ? remove
if [ -f "/media/fat/_Console/GameboyColor.mgl" ] 
then
   rm -r "/media/fat/_Console/GameboyColor.mgl"
fi
#wonderswan color mgl ? remove
if [ -f "/media/fat/_Console/WonderSwan Color.mgl" ] 
then
   rm -r "/media/fat/_Console/WonderSwan Color.mgl"
fi
#obsolete G&W
if [ -f "/media/fat/_Console/GnW_20220606.rbf" ] 
then
   rm -r "/media/fat/_Console/GnW_20220606.rbf"
fi

echo "Completed."
