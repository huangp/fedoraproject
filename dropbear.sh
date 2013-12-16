#!/bin/sh
f17=10.64.27.27

f18=10.64.27.224

f19=10.64.27.13

cmd="ssh cloud-user@"

if [ "$1" -eq "17" ]
then
    $cmd$f17
elif [ "$1" -eq "18" ]
then
    $cmd$f18
elif [ "$1" -eq "19" ]
then
    $cmd$f19
fi
  
exit
