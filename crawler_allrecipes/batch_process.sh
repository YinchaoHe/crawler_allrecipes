#!/bin/bash
#This script is use to split a big scraping processing into several small scraping tasks.
echo "Please enter start recipe_ID and end recipe_ID -> "
read start end
if [[ "$start" =~ ^-?[0-9]+$ ]]; then
	if [[ "$end" =~ ^-?[0-9]+$ ]];then
		interval=`expr $end  - $start`
		while [ "$interval" -gt 1000 ]; do
			interval=$(($interval / 2))
		done
		prestopsign=$start
		stopsign=$(($start + $interval))
		while [ $stopsign -le $end ]; do			
			python crawler.py -s $prestopsign -e $stopsign
			prestopsign=$stopsign
			stopsign=$(($prestopsign + $interval))
		done
		if [ $prestopsign -lt $end ];then
			python crawler.py -s $prestopsign -e $end
		fi
	else
		echo "please enter the end recipe_ID"
	fi
else
	echo "please enter the start recipe_ID"
fi
