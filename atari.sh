 #!/bin/bash  

source ./folders/functions.sh

echo "alt : $AltSourceRoot" >/dev/null

OutputRoot=$1

#echo "OutputRoot : $OutputRoot"

MainDir="_Atari"

cd $OutputRoot

create "$MainDir"

orientation=$2

if [ -z "$orientation" ] || [ "$orientation" = "V" ];
then
   #special_echo "\$orientation is empty or V"
   addgame "Breakout (TTL).mra" "_Breakout"
   addgame "Breakout.mra" "_Breakout"
   addgame "Centipede (Rev 3).mra" "_Centipede"
   addgame "Centipede (Rev 4).mra" "_Centipede"
   addgame "Centipede.mra" "_Centipede"
   addgame "Super Breakout (Rev 04).mra" "_Super Breakout"
   addgame "Super Breakout.mra" "_Super Breakout"
   addgame "Super Xevious.mra" "_Xevious"
   addgame "Tron.mra" "_Tron"
   addgame "Xevious.mra" "_Xevious"
fi
if [ -z "$orientation" ] || [ "$orientation" = "H" ];
then
   #special_echo "\$orientation is empty or H"
   addgame "Asteroids Deluxe.mra" "_Asteroids Deluxe"
   addgame "Asteroids.mra" "_Asteroid"
   addgame "Black Widow.mra" "_Black Widow"
   addgame "Canyon Bomber.mra" "_Canyon Bomber"
   addgame "Discs of Tron.mra" "_Disc of Tron"
   addgame "Dominos.mra" "_Dominos"
   addgame "Food Fight (Rev 3).mra" "_Food Fight"
   addgame "Food Fight.mra" "_Food Fight"
   addgame "Gauntlet (rev 14).mra" "_Gauntlet"
   addgame "Gauntlet II.mra" "_Gauntlet II"
   addgame "Gravitar (Ver 3).mra" "_Gravitar"
   addgame "Gravitar.mra" "_Gravitar"
   addgame "Indiana Jones.mra" "_Indiana Jones"
   addgame "Lunar Battle (Prototype).mra" "_Lunar Battle"
   addgame "Lunar Battle.mra" "_Lunar Battle"
   addgame "Lunar Lander.mra" "_Lunar Lander"
   addgame "Missile Command (rev 1).mra" "_Missile_Command"
   addgame "Missile Command (rev 2).mra" "_Missile_Command"
   addgame "Missile Command (rev 3).mra" "_Missile_Command"
   addgame "Peter Pack Rat.mra" "_Peter Pack Rat"
   addgame "Space Race [TTL].mra" "_Space Race"
   addgame "Space Race.mra" "_Space Race"
   addgame "Sprint 1.mra" "_Sprint 1"
   addgame "Sprint 2.mra" "_Sprint 2"
   addgame "Subs.mra" "_Subs"
   addgame "Vindicators Part II (rev 3).mra" "_Vindicators part II"

fi




exit 0