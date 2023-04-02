# redirect stdout/stderr to a file
#exec >run.txt 2>&1

exec 3>&1
special_echo () {
    echo "$@" >&3
}
exec &>/dev/null

launchdir=$1
#special_echo "launchdir $launchdir"

special_echo "Cleaning console mgl"

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

special_echo "Completed."
