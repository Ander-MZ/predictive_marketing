#!/bin/bash

echo Evaluating Model 0

python newModelSelector.py -i $1 -t ALL -m 0 -n 1 | tail -3 > ../results/out_M=0_N=1.txt 

python newModelSelector.py -i $1 -t ALL -m 0 -n 2 | tail -3 > ../results/out_M=0_N=2.txt

python newModelSelector.py -i $1 -t ALL -m 0 -n 3 | tail -3 > ../results/out_M=0_N=3.txt

python newModelSelector.py -i $1 -t ALL -m 0 -n 4 | tail -3 > ../results/out_M=0_N=4.txt 

python newModelSelector.py -i $1 -t ALL -m 0 -n 5 | tail -3 > ../results/out_M=0_N=5.txt

python newModelSelector.py -i $1 -t ALL -m 0 -n 6 | tail -3 > ../results/out_M=0_N=6.txt


echo Evaluating Model 1

python newModelSelector.py -i $1 -t ALL -m 1 -n 1 | tail -3 > ../results/out_M=1_N=1.txt

python newModelSelector.py -i $1 -t ALL -m 1 -n 2 | tail -3 > ../results/out_M=1_N=2.txt

python newModelSelector.py -i $1 -t ALL -m 1 -n 3 | tail -3 > ../results/out_M=1_N=3.txt

python newModelSelector.py -i $1 -t ALL -m 1 -n 4 | tail -3 > ../results/out_M=1_N=4.txt

python newModelSelector.py -i $1 -t ALL -m 1 -n 5 | tail -3 > ../results/out_M=1_N=5.txt

python newModelSelector.py -i $1 -t ALL -m 1 -n 6 | tail -3 > ../results/out_M=1_N=6.txt


echo Evaluating Model 2

python newModelSelector.py -i $1 -t ALL -m 2 -n 1 | tail -3 > ../results/out_M=2_N=1.txt

python newModelSelector.py -i $1 -t ALL -m 2 -n 2 | tail -3 > ../results/out_M=2_N=2.txt

python newModelSelector.py -i $1 -t ALL -m 2 -n 3 | tail -3 > ../results/out_M=2_N=3.txt

python newModelSelector.py -i $1 -t ALL -m 2 -n 4 | tail -3 > ../results/out_M=2_N=4.txt

python newModelSelector.py -i $1 -t ALL -m 2 -n 5 | tail -3 > ../results/out_M=2_N=5.txt

python newModelSelector.py -i $1 -t ALL -m 2 -n 6 | tail -3 > ../results/out_M=2_N=6.txt
