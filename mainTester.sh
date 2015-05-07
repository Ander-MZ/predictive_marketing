#!/bin/bash

echo "Evaluating models"

echo "04-08"

bash tester.sh ~/Storage/data/2013-04-01_2013-08-01_data_sorted.csv 04-08

echo "04-09"

python dataProfiler.py -i ~/Storage/data/2013-04-01_2013-09-01_data_sorted.csv 

bash tester.sh ~/Storage/data/2013-04-01_2013-09-01_data_sorted.csv 04-09