#!/bin/sh

# when the script is run, the complete simulation will be run, and will take some hours.
# modify the script accordingly, to change the parameters of the network. 
# p = power
# m = bandwidth
# i = time 

### please note: you have to manually change the controller in a different terminal everytime you run this.
### I used two of those -- simple_switch.py and sec_switch.py, which are included in the repo.
### run like this: ~\ryu$ ./bin/ryu-manager <controller-script>.py
for p in 100 150;
do
    for m in 1.0 1.5 2.0;
    do
        mkdir "$p"_"$m"_n;
        for i in `seq 40 20 140`;
        do
            # pass simulation time, bandwidth, and power to the network
            python topo.py "$i" "$m" "$p";
            # wait for the network simulation to end
            sleep "$i"+1;
            mn -c;
            sleep 3;
            # after one run we have a folder of the form power_bandwidth_n
            # this folder will contain the average delays for every client under their name.
            for j in `seq 1 1 5`;
            do
                k=`cat vout"$j" | wc -l`;
                if [ "$k" -eq 0 ];
                then
                    # sometimes we do not get any replies for some clients, because of DDoS. 
                    # therefore I have assumed 5000 millis as infinity.
                    echo "5000" >> delays_"$i";
                else
                    sum=`cat vout"$j" | numsum`;
                    echo "$sum/$k" | bc -l >> delays_"$i";
                fi
            done
            rm vout*;
            mv delays_* "$p"_"$m"_n;
            mv dns_"$m"_"$i" "$p"_"$m"_n;
        done
    done
done
