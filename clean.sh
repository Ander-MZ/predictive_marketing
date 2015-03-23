#!/bin/bash

res1=`date +%s`

echo "Cleaning rows with noise"

awk -F "," '$8 ~ /^[0-9]*$/{print $0}' "$1" > ../results/query_clean.csv

echo "Sorting by pan and date (ascending)"

sort -t "," -k1 -nk4 -nk5 -nk6 ../results/query_clean.csv > ../results/query_sorted.csv && rm ../results/query_clean.csv

(echo "pan,amount,mcc,month,day,hour,dow,com_id" ; cat ../results/query_sorted.csv) > ../results/temp.csv && mv ../results/temp.csv ../results/query_sorted.csv 

echo "Grouping data by supplied key:" "$2"

python groupBy.py -i ../results/query_sorted.csv -o ../results/groupedData.csv -c "$2"

echo "Sorting output"

awk -F "," '{print NF,$0}' ../results/groupedData.csv | sort -rnk1,1 | cut -d ' ' -f 2- > ../results/temp.csv && mv ../results/temp.csv ../results/groupedData.csv 

echo "Creating transition matrix"

python createTransitionMatrix.py -i ../results/groupedData.csv

res2=`date +%s`

dt=$(echo "$res2 - $res1" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)

printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds