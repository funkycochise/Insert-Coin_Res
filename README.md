# Coin-Op for Mister FPGA

Coin_op is a folder created inside _Arcade
it needs update_all to be run first to get all mra populated in /media/fat/_Arcade
the script creates symbolic link of the mras to have them sorted by Manufacturer/Systems
to name a few :
_Atari
_Cave68K
_CPS1
_Crazy Kong
_Pacman

It will also install additional resources (rbf, mras) 
Sega System 1/2, Neogeo MVS, toaplan, nemesis, armedf, batrider, etc...

Installation :
1. Run update_all script with alternatives option activated for both regular and JT repository.
This should create you the /_Arcade/alternatives folder

2. unzip complete_scripts.7z install_coinop.sh into /media/fat/Scripts and run install_coinop.sh from OSD or ssh
3. if you want to update additionnal Console cores, just put update_console.sh in same directory as install_coinop.sh

update_console.sh will update/Intall Saturn, PSX, SGB console cores
update_main_mister.sh will install custom Mister to remove progress bar when loading roms
