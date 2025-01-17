#!/usr/bin/env python2.7

# Copyright 2022 Ross Vicario



# if can't import rosbag error, use "pip install bagpy"

import rosbag

import sys 

from datetime import datetime as DT

from azim_trans import AzimuthalProjection



# input arguments: abs path to source file and abs path to destination folder

filepath = r'{}'.format(sys.argv[1])

dest = r'{}'.format(sys.argv[2])

# append destination folder with filename

dest += "/" + filepath.split('/')[-1]

bag = rosbag.Bag(filepath)



# output 3 files: filename_fix.csv, _pos.csv, and _time.csv

# these 3 files each contain part of the data recorded by the GPS

with open(dest +  '_fix.csv', 'w') as fixfile, \
    open(dest + '_pos.csv', 'w') as posfile, \
    open(dest + '_time.csv', 'w') as timefile:

    fixfile.write('type,mode_selection,mode,satellite_count\n')

    posfile.write('latitude,longitude,x(meter),y(meter),altitude,separation,fix_3d\n')

    # the gps time is in EST

    # question: why is it called "utc_time" internally?

    timefile.write('device_time,gps_time_EST\n')

    projection_calibrated = False

    for topic, msg, t in bag.read_messages():

        if(topic == '/gnss/fix'):

            # if mode is 0, the device has no satellite connection

            # if no sat connection, the others don't publish anything

            if msg.mode == 0: # correct for missing entries by printing "NO_FIX"

                posfile.write("NO_FIX,NO_FIX,NO_FIX,NO_FIX,NO_FIX,NO_FIX,NO_FIX\n")

                timefile.write("NO_FIX,NO_FIX\n")

            fixfile.write("{}.format(msg.type),{}.format(msg.mode_selection),{}.format(msg.mode),{}.format(msg.satellite_count)\n")

        elif(topic == '/gnss/position'):

            if projection_calibrated == False:

                AP = AzimuthalProjection(msg.latitude, msg.longitude)
                
                projection_calibrated = True

            x,y = AP.latlon_to_xy(msg.latitude, msg.longitude)
            string = "{}.format(msg.latitude:0.8f),{}.format(msg.longitude:0.8f)," \
                + "{}.format(x),{}.format(y),{}.format(msg.altitude:0.8f)," \
                + "{}.format(msg.separation:0.8f),{}.format(msg.fix_3d)\n"
            posfile.write(string)
        elif(topic == '/gnss/time'):

            # use datetime to convert from epoch time to more standardized form

            internal_time = DT.fromtimestamp(t.to_sec())

            gps_time = DT.fromtimestamp(msg.utc_time.to_sec())

            timefile.write("{}.format(internal_time),{}.format(gps_time)\n")
