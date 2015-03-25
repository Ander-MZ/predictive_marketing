#!/bin/bash

rm -r ../results/img_m0
mkdir ../results/img_m0

bash matrix.sh 04 0
bash matrix.sh 05 0
bash matrix.sh 06 0

rm -r ../results/img_m1
mkdir ../results/img_m1

bash matrix.sh 04 1
bash matrix.sh 05 1
bash matrix.sh 06 1

rm -r ../results/img_m2
mkdir ../results/img_m2

bash matrix.sh 04 2
bash matrix.sh 05 2
bash matrix.sh 06 2

rm -r ../results/img_total
mkdir ../results/img_total

tar -cvf ../results/img_m0.tar ../results/img_m0
tar -cvf ../results/img_m1.tar ../results/img_m1
tar -cvf ../results/img_m2.tar ../results/img_m2

cp ../results/img_m*.tar ./img_total/

tar -cvf ../results/img_total.tar ../results/img_total
