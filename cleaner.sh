#!/bin/bash

echo "Working on file: " "$1" " on column " "$2"

echo "Removing extra lines (DB prints)"

sed -i '$ d' ../results/${1}_first.csv

sed -i '$ d' ../results/${1}_last.csv

sed -i '1 d' ../results/${1}_first.csv

sed -i '1 d' ../results/${1}_last.csv


echo "Cleaning rows from incorrect values"

awk -F "," '$9 ~ /^[0-9]*$/{print $0}' ../results/${1}_first.csv > ../results/${1}_first_cleaned.csv

awk -F "," '$9 ~ /^[0-9]*$/{print $0}' ../results/${1}_last.csv > ../results/${1}_last_cleaned.csv


echo "Grouping rows by pan and then sorting by date"

sort -T ~/Storage -t "," -k1,1 -k4n -k5n -k6n -k7n ../results/${1}_first_cleaned.csv > ../results/${1}_first_sorted.csv

sort -T ~/Storage -t "," -k1,1 -k4n -k5n -k6n -k7n ../results/${1}_last_cleaned.csv > ../results/${1}_last_sorted.csv


echo "Adding header to files"

(echo "pan,amount,mcc,month,day,hour,min,dow,com_id" ; cat ../results/${1}_first_sorted.csv) > ../results/temp.csv && mv ../results/temp.csv ../results/${1}_first_sorted.csv

(echo "pan,amount,mcc,month,day,hour,min,dow,com_id" ; cat ../results/${1}_last_sorted.csv) > ../results/temp.csv && mv ../results/temp.csv ../results/${1}_last_sorted.csv


echo "Grouping by pan and extracting" "$2"

python groupBy.py -i ../results/${1}_first_sorted.csv -o ../results/${1}_${2}_by_pan_first.csv -c "$2"

python groupBy.py -i ../results/${1}_last_sorted.csv -o ../results/${1}_${2}_by_pan_last.csv -c "$2"


echo "Sorting grouped data by number of transactions (descending)"

awk -F "," '{print NF,$0}' ../results/${1}_${2}_by_pan_first.csv | sort -T ~/Storage -rnk1,1 | cut -d ' ' -f 2- > ../results/temp.csv && mv ../results/temp.csv ../results/${1}_${2}_by_pan_first.csv 

awk -F "," '{print NF,$0}' ../results/${1}_${2}_by_pan_last.csv | sort -T ~/Storage -rnk1,1 | cut -d ' ' -f 2- > ../results/temp.csv && mv ../results/temp.csv ../results/${1}_${2}_by_pan_last.csv 
