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
            echo $((sum/k)) >> simple$i;
        fi
    done
    rm vout*
done

