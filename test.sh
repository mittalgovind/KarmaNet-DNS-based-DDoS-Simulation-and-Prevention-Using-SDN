#!/bin/bash

k=`cat vout1 | wc -l`;
sum=`cat vout1 | numsum `;
echo $k
echo $sum
echo $sum/$k | bc -l