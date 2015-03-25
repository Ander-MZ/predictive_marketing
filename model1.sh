#!/bin/bash

echo "Order: " "$1"

python createTransitionMatrix.py -t ../results/04_mcc_by_pan_first.csv -e ../results/04_mcc_by_pan_last.csv -r ../results/04_mcc_results_m${1}.csv -o "$1"
python createTransitionMatrix.py -t ../results/04_com_id_by_pan_first.csv -e ../results/04_com_id_by_pan_last.csv -r ../results/04_com_id_results_m${1}.csv -o "$1"

python createTransitionMatrix.py -t ../results/05_mcc_by_pan_first.csv -e ../results/05_mcc_by_pan_last.csv -r ../results/05_mcc_results_m${1}.csv -o "$1"
python createTransitionMatrix.py -t ../results/05_com_id_by_pan_first.csv -e ../results/05_com_id_by_pan_last.csv -r ../results/05_com_id_results_m${1}.csv -o "$1"

python createTransitionMatrix.py -t ../results/06_mcc_by_pan_first.csv -e ../results/06_mcc_by_pan_last.csv -r ../results/06_mcc_results_m${1}.csv -o "$1"
python createTransitionMatrix.py -t ../results/06_com_id_by_pan_first.csv -e ../results/06_com_id_by_pan_last.csv -r ../results/06_com_id_results_m${1}.csv -o "$1"