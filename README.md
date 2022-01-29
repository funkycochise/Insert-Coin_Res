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
Sega System 1/2, Neogeo MVS, toaplan
Note : No roms are downloaded nor Jotego's jtbeta.zip

Installation :
1. Run update_all script with alternatives option activated for both regular and JT repository.
This should create you the /_Arcade/alternatives folder

2. copy install_coinop.sh into /media/fat/Scripts and run it from OSD
