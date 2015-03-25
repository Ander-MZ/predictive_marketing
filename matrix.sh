#!/bin/bash

python dataSegmentation.py -i ../results/04_first_sorted.csv -r ../results/04_mcc_results_m0.csv
python dataSegmentation.py -i ../results/04_first_sorted.csv -r ../results/04_com_id_results_m0.csv

python dataSegmentation.py -i ../results/05_first_sorted.csv -r ../results/05_mcc_results_m0.csv
python dataSegmentation.py -i ../results/05_first_sorted.csv -r ../results/05_com_id_results_m0.csv

python dataSegmentation.py -i ../results/06_first_sorted.csv -r ../results/06_mcc_results_m0.csv
python dataSegmentation.py -i ../results/06_first_sorted.csv -r ../results/06_com_id_results_m0.csv