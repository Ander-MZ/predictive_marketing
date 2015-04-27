#!/bin/bash

echo Evaluating all - Model 0

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 1 -m ${2}_0_N=1_ALL | tail -3 > ../results/${2}_out_0_N=1_ALL.txt 

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 2 -m ${2}_0_N=2_ALL | tail -3 > ../results/${2}_out_0_N=2_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 3 -m ${2}_0_N=3_ALL | tail -3 > ../results/${2}_out_0_N=3_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 4 -m ${2}_0_N=4_ALL | tail -3 > ../results/${2}_out_0_N=4_ALL.txt 

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 5 -m ${2}_0_N=5_ALL | tail -3 > ../results/${2}_out_0_N=5_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 1000 -1 1 -2 1 -n 6 -m ${2}_0_N=6_ALL | tail -3 > ../results/${2}_out_0_N=6_ALL.txt

echo Evaluating any - Model 0

python newModelSelector.py -i $1 -t ANY -0 1000 -1 1 -2 1 -n 2 -m ${2}_0_N=2_ANY | tail -3 > ../results/${2}_out_0_N=2_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 1000 -1 1 -2 1 -n 3 -m ${2}_0_N=3_ANY | tail -3 > ../results/${2}_out_0_N=3_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 1000 -1 1 -2 1 -n 4 -m ${2}_0_N=4_ANY | tail -3 > ../results/${2}_out_0_N=4_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 1000 -1 1 -2 1 -n 5 -m ${2}_0_N=5_ANY | tail -3 > ../results/${2}_out_0_N=5_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 1000 -1 1 -2 1 -n 6 -m ${2}_0_N=6_ANY | tail -3 > ../results/${2}_out_0_N=6_ANY.txt

#

echo Evaluating all - Model 1

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 1 -m ${2}_1_N=1_ALL | tail -3 > ../results/${2}_out_1_N=1_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 2 -m ${2}_1_N=2_ALL | tail -3 > ../results/${2}_out_1_N=2_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 3 -m ${2}_1_N=3_ALL | tail -3 > ../results/${2}_out_1_N=3_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 4 -m ${2}_1_N=4_ALL | tail -3 > ../results/${2}_out_1_N=4_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 5 -m ${2}_1_N=5_ALL | tail -3 > ../results/${2}_out_1_N=5_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1000 -2 1 -n 6 -m ${2}_1_N=6_ALL | tail -3 > ../results/${2}_out_1_N=6_ALL.txt

echo Evaluating any - Model 1

python newModelSelector.py -i $1 -t ANY -0 10 -1 1000 -2 1 -n 2 -m ${2}_1_N=2_ANY | tail -3 > ../results/${2}_out_1_N=2_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1000 -2 1 -n 3 -m ${2}_1_N=3_ANY | tail -3 > ../results/${2}_out_1_N=3_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1000 -2 1 -n 4 -m ${2}_1_N=4_ANY | tail -3 > ../results/${2}_out_1_N=4_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1000 -2 1 -n 5 -m ${2}_1_N=5_ANY | tail -3 > ../results/${2}_out_1_N=5_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1000 -2 1 -n 6 -m ${2}_1_N=6_ANY | tail -3 > ../results/${2}_out_1_N=6_ANY.txt

#

echo Evaluating all - Model 2

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 1 -m ${2}_2_N=1_ALL | tail -3 > ../results/${2}_out_2_N=1_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 2 -m ${2}_2_N=2_ALL | tail -3 > ../results/${2}_out_2_N=2_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 3 -m ${2}_2_N=3_ALL | tail -3 > ../results/${2}_out_2_N=3_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 4 -m ${2}_2_N=4_ALL | tail -3 > ../results/${2}_out_2_N=4_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 5 -m ${2}_2_N=5_ALL | tail -3 > ../results/${2}_out_2_N=5_ALL.txt

python newModelSelector.py -i $1 -t ALL -0 10 -1 1 -2 1000 -n 6 -m ${2}_2_N=6_ALL | tail -3 > ../results/${2}_out_2_N=6_ALL.txt

echo Evaluating any - Model 2

python newModelSelector.py -i $1 -t ANY -0 10 -1 1 -2 1000 -n 2 -m ${2}_0_N=2_ANY | tail -3 > ../results/${2}_out_2_N=2_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1 -2 1000 -n 3 -m ${2}_0_N=3_ANY | tail -3 > ../results/${2}_out_2_N=3_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1 -2 1000 -n 4 -m ${2}_0_N=4_ANY | tail -3 > ../results/${2}_out_2_N=4_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1 -2 1000 -n 5 -m ${2}_0_N=5_ANY | tail -3 > ../results/${2}_out_2_N=5_ANY.txt

python newModelSelector.py -i $1 -t ANY -0 10 -1 1 -2 1000 -n 6 -m ${2}_0_N=6_ANY | tail -3 > ../results/${2}_out_2_N=6_ANY.txt
