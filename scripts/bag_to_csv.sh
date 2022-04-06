#!/bin/bash

# get to the right folder
D="$(find ~ -name gps_drift 2>/dev/null)"
cd "$D"

rm -Rf csv 
mkdir csv 

# get our python script
P="$(find . -name bags_to_csv.py 2>/dev/null)"

echo "$P"


# paste m1_gps_2022-02-17-16-30-00.bag_time.csv m1_gps_2022-02-17-16-30-00.bag_pos.csv m1_gps_2022-02-17-16-30-00.bag_fix.csv -d "," > m1_gps_2022-02-17-16-30-00.csv
# paste m2_gps_2022-02-17-16-30-00.bag_time.csv m2_gps_2022-02-17-16-30-00.bag_pos.csv m2_gps_2022-02-17-16-30-00.bag_fix.csv -d "," > m2_gps_2022-02-17-16-30-00.csv
# paste m3_gps_2022-02-17-16-30-00.bag_time.csv m3_gps_2022-02-17-16-30-00.bag_pos.csv m3_gps_2022-02-17-16-30-00.bag_fix.csv -d "," > m3_gps_2022-02-17-16-30-00.csv
# paste m4_gps_2022-02-17-16-30-00.bag_time.csv m4_gps_2022-02-17-16-30-00.bag_pos.csv m4_gps_2022-02-17-16-30-00.bag_fix.csv -d "," > m4_gps_2022-02-17-16-30-00.csv
