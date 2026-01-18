#!/bin/bash

function dl {
name=$1
file=$2

if [ ! -f "$file" ]; then
  echo "Getting latest default Insert-Coin $name"
  curl "https://raw.githubusercontent.com/funkycochise/Insert-Coin_Res/main/$name" --insecure -o "$2" 
fi
}

dl "setup.ini" "/media/fat/Scripts/#insertcoin/setup.ini"
dl "names.ini" "/media/fat/Scripts/#insertcoin/names.ini"

cd /media/fat/Scripts/#insertcoin
./run.sh | tee output.log
