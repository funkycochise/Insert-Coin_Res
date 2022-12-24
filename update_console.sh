# redirect stdout/stderr to a file
#exec >run.txt 2>&1

exec 3>&1
special_echo () {
    echo "$@" >&3
}
exec &>/dev/null

launchdir=$1
#special_echo "launchdir $launchdir"

special_echo "Getting latest console cores"

CONSOLE=/media/fat/_Console/

wget https://raw.githubusercontent.com/funkycochise/Insert-Coin_Res/main/console.zip
if test -f "./console.zip"; then
   unzip console.zip >/dev/null
   rm -r ./console.zip >/dev/null
   special_echo "PSX"
   rm -r $CONSOLE/PSX*.rbf >/dev/null
   mv ./PSX*.rbf $CONSOLE
   touch $CONSOLE/PSX*.rbf >/dev/null
   special_echo "Saturn"
   rm -r $CONSOLE/Saturn*.rbf >/dev/null
   mv ./Saturn*.rbf $CONSOLE
   touch $CONSOLE/Saturn*.rbf >/dev/null
   special_echo "S32X"
   rm -r $CONSOLE/S32X*.rbf >/dev/null
   mv ./S32X*.rbf $CONSOLE
   touch $CONSOLE/S32X*.rbf >/dev/null
   special_echo "SGB"
   rm -r $CONSOLE/SGB*.rbf >/dev/null
   mv ./SGB*.rbf $CONSOLE
   touch $CONSOLE/SGB*.rbf >/dev/null
fi

#clean obsolete core
if test -f "/media/fat/_Console/Casio_PV-1000_20220804.rbf"; then
   rm -r /media/fat/_Console/Casio_PV-1000_20220804.rbf >/dev/null
fi
if test -f "/media/fat/_Console/SMS_20220811.rbf"; then
rm -r /media/fat/_Console/SMS_20220620.rbf
fi
if  test -f "/media/fat/_Console/SMS_20221014.rbf"; then
rm -r /media/fat/_Console/SMS_20220811.rbf
fi

special_echo "Completed."
