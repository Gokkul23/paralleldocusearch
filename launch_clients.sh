#!/bin/sh
first=$1
for (( i = 0; i < $first; i++ )) 
do
	open -a Terminal.app spawn_client.sh
done