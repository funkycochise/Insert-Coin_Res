SrcDir=/media/fat/games
OutDir=/media/usb0/games

function symlinkfolder {
echo "creating $OutDir/$1";
rm -r "$OutDir/$1" >/dev/null
ln -s "SrcDir/$1"  "/$OutDir/$1"
}

echo "Creating symlink on usb"

symlinkfolder AcornAtom
symlinkfolder AliceMC10
symlinkfolder Altair8800
symlinkfolder Amiga
symlinkfolder Amstrad
symlinkfolder "Amstrad PCW"
symlinkfolder ao486
symlinkfolder Apogee
symlinkfolder Apple-I
symlinkfolder Apple-II
symlinkfolder Aquarius
symlinkfolder Arcadia
symlinkfolder Archie
symlinkfolder Astrocade
symlinkfolder Atari2600
symlinkfolder Atari5200
symlinkfolder Atari7800
symlinkfolder Atari800
symlinkfolder AtariLynx
symlinkfolder AtariST
symlinkfolder Atom
symlinkfolder AY-3-8500
symlinkfolder BBCMicro
symlinkfolder BK0011M
symlinkfolder C16
symlinkfolder C64
symlinkfolder ChannelF
symlinkfolder Chip8
symlinkfolder CO2650
symlinkfolder CoCo2
symlinkfolder CoCo3
symlinkfolder Coleco
symlinkfolder EDSAC
symlinkfolder Electron
symlinkfolder Galaksija
symlinkfolder GameBoy
symlinkfolder GAMEBOY2P
symlinkfolder "Game & Watch"
symlinkfolder GBA
symlinkfolder GBA2P
symlinkfolder Genesis
symlinkfolder hbmame
symlinkfolder HT1080Z
symlinkfolder Intellivision
symlinkfolder Interact
symlinkfolder Jaguar
symlinkfolder Jupiter
symlinkfolder Laser
symlinkfolder MacPlus
symlinkfolder mame
symlinkfolder MegaCD
symlinkfolder mo
symlinkfolder MSX
symlinkfolder MultiComp
symlinkfolder NEOGEO
symlinkfolder NES
symlinkfolder Odyssey2
symlinkfolder Ondra_SPO186
symlinkfolder ORAO
symlinkfolder Oric
symlinkfolder PDP1
symlinkfolder PET2001
symlinkfolder PMD85
symlinkfolder QL
symlinkfolder rx78
symlinkfolder SamCoupe
symlinkfolder SharpMZ
symlinkfolder SMS
symlinkfolder SNES
symlinkfolder "Sord M5"
symlinkfolder SparcStation
symlinkfolder Spectrum
symlinkfolder SPMX
symlinkfolder SVI328
symlinkfolder TGFX16
symlinkfolder TI-99_4A
symlinkfolder TomyScramble
symlinkfolder TRS-80
symlinkfolder TSConf
symlinkfolder UK101
symlinkfolder vc4000
symlinkfolder Vector06
symlinkfolder Vectrex
symlinkfolder VIC20
symlinkfolder WonderSwan
symlinkfolder X68000
symlinkfolder zx48
symlinkfolder ZX81
symlinkfolder ZXNext
