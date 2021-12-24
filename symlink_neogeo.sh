SrcDir=/media/fat/games/NEOGEO
OutDir=/media/fat/games/mame

#echo "$SrcDir";

for completefile in $SrcDir/*.zip;
do
   file=${completefile##*/}
   rm "$OutDir/$file"
   echo "$SrcDir/$file -> $OutDir/$file";
   ln -s "$SrcDir/$file" "$OutDir/$file";
done
