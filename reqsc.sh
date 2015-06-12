#!/bin/bash

n_messages=$(
    for i in $(seq 1 10); do
        echo $(($i * 10000))
    done
)

for i in $n_messages; do
    python3.4 client -t tcp -s 100 -n $i
done
