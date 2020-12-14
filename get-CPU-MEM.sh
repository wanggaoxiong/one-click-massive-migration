#! /bin/bash
mem=$(cat /proc/meminfo|grep "MemTotal" |tr -cd "[0-9]" |awk '{print int($1/1024/1024+0.5)}')
cpu=$(cat /proc/cpuinfo |grep "cpu cores" |wc -l)
a=$(echo "$cpu-:-$mem")
echo "$a"
