#!/bin/sh

for p in 150;
do
    for m in 1.5;
    do
        mkdir "$p"_"$m"_n;
        for i in 60;
        do
            python topo.py "$i" "$m" "$p";
            sleep "$i"+1;
            mn -c;
            sleep 3;
            for j in `seq 1 1 5`;
            do
                k=`cat vout"$j" | wc -l`;
                if [ "$k" -eq 0 ];
                then
                    echo "5000" >> simple"$i";
                else
                    sum=`cat vout"$j" | numsum`;
                    echo "$sum/$k" | bc -l >> simple"$i";
                fi
            done
            rm vout*;
            mv simple* "$p"_"$m"_n;
            mv dns_"$m"_"$i" "$p"_"$m"_n;
        done
    done
done