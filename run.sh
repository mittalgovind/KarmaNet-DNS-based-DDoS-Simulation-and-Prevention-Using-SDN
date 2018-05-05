#!/bin/sh

for i in `seq 20 20 120`;
do
    python topo.py $i;
    sleep $i+1;
    mn -c;
    sleep 3;
    for j in `seq 1 1 5`;
    do
        k=`cat vout$j | wc -l`;
        if [ $k -eq 0 ];
        then
            echo "0" >> simple$i;
        else
            sum=`cat vout$j | numsum -i`;
            echo $sum/$k | bc -l >> simple$i;
            bash;
        fi
    done
    rm vout*;
    mkdir 50_0.5_n;
    mv simple* 50_0.5_n;
    mv dns_* 50_0.5_n;
done
cd 
