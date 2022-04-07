#!/bin/bash

# constraint: must be named gps_drift
# get to the working directory
work_dir="$(find ~ -name gps_drift 2>/dev/null)" && cd $work_dir

# get rid of the old output folder & remake
rm -Rf csv_out
mkdir csv_out && cd csv_out

# get python script (constraint: must be in the gps_drift dir)
python_script="$(find $work_dir -name "bag_to_csv.py" 2>/dev/null)"
echo "SCRIPT    : $python_script"

for i in $(find $work_dir -name "m*.bag" 2>/dev/null); do
    echo "CONVERTING: $i"
    # start the python script with input file & destination
    # the python script creates 3 incomplete files
    python3 $python_script "$i" "$work_dir/csv_out"
    echo "MERGING   : $i"
    # collect the 3 incomplete files
    T="$(ls | grep "time")"
    P="$(ls | grep "pos")"
    F="$(ls | grep "fix")"

    # combine them with paste
    O="$(echo $T | sed 's/.bag_time//')"

    paste $T $P $F -d "," > $O
    # CLEANUP: remove the incomplete files
    rm $T $P $F
    echo "      DONE"
done
