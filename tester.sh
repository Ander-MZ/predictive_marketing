#!/bin/bash

echo Evaluating all - Model 0

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 1 -m 0_N=1_ALL > ../results/out_0_N=1_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 2 -m 0_N=2_ALL > ../results/out_0_N=2_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1000 -1 1 -2 1 -n 3 -m 0_N=3_ALL > ../results/out_0_N=3_ALL.txt

echo Evaluating any - Model 0

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1000 -1 1 -2 1 -n 1 -m 0_N=1_ANY > ../results/out_0_N=1_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1000 -1 1 -2 1 -n 2 -m 0_N=2_ANY > ../results/out_0_N=2_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1000 -1 1 -2 1 -n 3 -m 0_N=3_ANY > ../results/out_0_N=3_ANY.txt

#

echo Evaluating all - Model 1

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1000 -2 1 -n 1 -m 1_N=1_ALL > ../results/out_1_N=1_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1000 -2 1 -n 2 -m 1_N=2_ALL > ../results/out_1_N=2_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1000 -2 1 -n 3 -m 1_N=3_ALL > ../results/out_1_N=3_ALL.txt

echo Evaluating any - Model 1

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1000 -2 1 -n 1 -m 1_N=1_ANY > ../results/out_1_N=1_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1000 -2 1 -n 2 -m 1_N=2_ANY > ../results/out_1_N=2_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1000 -2 1 -n 3 -m 1_N=3_ANY > ../results/out_1_N=3_ANY.txt

#

echo Evaluating all - Model 2

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1 -2 1000 -n 1 -m 2_N=1_ALL > ../results/out_2_N=1_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1 -2 1000 -n 2 -m 2_N=2_ALL > ../results/out_2_N=2_ALL.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ALL -0 1 -1 1 -2 1000 -n 3 -m 2_N=3_ALL > ../results/out_2_N=3_ALL.txt

echo Evaluating any - Model 2

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1 -2 1000 -n 1 -m 0_N=1_ANY > ../results/out_1_N=1_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1 -2 1000 -n 2 -m 0_N=2_ANY > ../results/out_1_N=2_ANY.txt

python newModelSelector.py -i ../results/months/04-06_sorted_lite.csv -t ANY -0 1 -1 1 -2 1000 -n 3 -m 0_N=3_ANY > ../results/out_1_N=3_ANY.txt
