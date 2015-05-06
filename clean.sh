#!/bin/bash

res1=`date +%s`

echo "Working on file: " "$1"

echo "Removing extra lines (DB prints)"

sed -i '1 d' ~/Storage/data/${1}.csv # Remove first line

sed -i '$ d' ~/Storage/data/${1}.csv # Remove last line

echo "Cleaning rows from incorrect values"

awk -F "," '$10 ~ /^[0-9]*$/{print $0}' ~/Storage/data/${1}.csv > ~/Storage/data/${1}_cleaned.csv

echo "Grouping rows by pan and then sorting by date"

sort -T ~/Storage -t "," -k1,1 -k4,4n -k5,5n -k6,6n -k7,7n -k8,8n ~/Storage/data/${1}_cleaned.csv > ~/Storage/data/${1}_sorted.csv

echo "Adding header to file"

(echo "pan,amount,mcc,year,month,day,hour,min,dow,com_id" ; cat ~/Storage/data/${1}_sorted.csv) > ~/Storage/data/temp.csv && mv ~/Storage/data/temp.csv ~/Storage/data/${1}_sorted.csv

res2=`date +%s`

dt=$(echo "$res2 - $res1" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)

printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds