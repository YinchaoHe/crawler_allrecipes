#!/bin/bash
#This script is use to split a big scraping processing into several small scraping tasks.
echo "Please enter start recipe_ID, end recipe_ID, and index-> "
read start end index

interval=`expr $end  - $start`
while [ "$interval" -gt 1000 ]; do
  interval=$(($interval / 2))
done
prestopsign=$start
stopsign=$(($start + $interval))
while [ $stopsign -le $end ]; do
  python crawler_by_id.py -s $prestopsign -e $stopsign -i $index
  prestopsign=$stopsign
  stopsign=$(($prestopsign + $interval))
  index=$(($index + 1))
done

