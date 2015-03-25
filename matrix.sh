#!/bin/bash

echo "Working on file: " "$1" " with order: " "$2"

python dataSegmentation.py -i ../results/${1}_first_sorted.csv -r ../results/${1}_mcc_results_m${2}.csv
python dataSegmentation.py -i ../results/${1}_first_sorted.csv -r ../results/${1}_com_id_results_m${2}.csv

python exploration.py -i ../results/${1}_mcc_results_m${2}.csv
python exploration.py -i ../results/${1}_com_id_results_m${2}.csv

echo "Moving results to ~/results/img_m""$2"

cp ../results/*m${2}*.png ../results/img_m${2}