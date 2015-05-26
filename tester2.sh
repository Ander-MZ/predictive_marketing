#!/bin/bash

echo Evaluating all - Model 0

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 2 -m 0_N=2_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 3 -m 0_N=3_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 4 -m 0_N=4_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 5 -m 0_N=5_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 6 -m 0_N=6_ALL

#

echo Evaluating all - Model 1

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 1 -m 1_N=1_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 2 -m 1_N=2_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 3 -m 1_N=3_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 4 -m 1_N=4_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 5 -m 1_N=5_ALL 

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1000 -2 1 -n 6 -m 1_N=6_ALL 

echo Evaluating any - Model 1

#python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 1 -m 1_N=1_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 2 -m 1_N=2_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 3 -m 1_N=3_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 4 -m 1_N=4_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 5 -m 1_N=5_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1000 -2 1 -n 6 -m 1_N=6_ANY

#

echo Evaluating all - Model 2

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 1 -m 2_N=1_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 2 -m 2_N=2_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 3 -m 2_N=3_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 4 -m 2_N=4_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 5 -m 2_N=5_ALL

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ALL -0 10 -1 1 -2 1000 -n 6 -m 2_N=6_ALL

echo Evaluating any - Model 2

#python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 1 -m 0_N=1_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 2 -m 2_N=2_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 3 -m 2_N=3_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 4 -m 2_N=4_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 5 -m 2_N=5_ANY

python newModelSelector.py -i ../data/04-06_sorted_50M_lite.csv -t ANY -0 10 -1 1 -2 1000 -n 6 -m 2_N=6_ANY
