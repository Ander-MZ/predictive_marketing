 #!/bin/bash

echo "Extracting rows from database"

psql -d banamex -U eglobal -F "," -A -f queries/queryMonth_first.sql > results/month_first.csv

psql -d banamex -U eglobal -F "," -A -f queries/queryMonth_last.sql > results/month_last.csv


echo "Removing extra lines (DB prints)"

sed -i '$ d' results/month_first.csv

sed -i '$ d' results/month_last.csv

sed -i '1 d' results/month_first.csv

sed -i '1 d' results/month_last.csv


echo "Cleaning rows from incorrect values"

awk -F "," '$9 ~ /^[0-9]*$/{print $0}' results/month_first.csv > results/month_first_cleaned.csv

awk -F "," '$9 ~ /^[0-9]*$/{print $0}' results/month_last.csv > results/month_last_cleaned.csv


echo "Grouping rows by pan and then sorting by date"

sort -T ~/tmp/ -t "," -k1,1 -k4n -k5n -k6n -k7n results/month_first_cleaned.csv > results/month_first_sorted.csv

sort -T ~/tmp/ -t "," -k1,1 -k4n -k5n -k6n -k7n results/month_last_cleaned.csv > results/month_last_sorted.csv


echo "Adding header to files"

(echo "pan,amount,mcc,month,day,hour,min,dow,com_id" ; cat results/month_first_sorted.csv) > results/temp.csv && mv results/temp.csv results/month_first_sorted.csv

(echo "pan,amount,mcc,month,day,hour,min,dow,com_id" ; cat results/month_last_sorted.csv) > results/temp.csv && mv results/temp.csv results/month_last_sorted.csv


echo "Grouping by pan and extracting" "$1"

python groupBy.py -i results/month_first_sorted.csv -o results/group_by_pan_first.csv -c "$1"

python groupBy.py -i results/month_last_sorted.csv -o results/group_by_pan_last.csv -c "$1"


echo "Sorting grouped data by number of transactions (descending)"

awk -F "," '{print NF,$0}' results/group_by_pan_first.csv | sort -rnk1,1 | cut -d ' ' -f 2- > results/temp.csv && mv results/temp.csv results/group_by_pan_first.csv 

awk -F "," '{print NF,$0}' results/group_by_pan_last.csv | sort -rnk1,1 | cut -d ' ' -f 2- > results/temp.csv && mv results/temp.csv results/group_by_pan_last.csv 




