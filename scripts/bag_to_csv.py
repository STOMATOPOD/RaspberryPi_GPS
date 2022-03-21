import rosbag
import sys

filename = sys.argv[1]
bag = rosbag.Bag(filename)

with open(filename + '_fix.csv', 'w') as fixfile, \
    open(filename + '_pos.csv', 'w') as posfile, \
    open(filename + '_time.csv', 'w') as timefile:
    fixfile.write('time,type,mode_selection,mode,satellite_count\n')
    posfile.write('time,latitude,longitude,altitude,separation,fix_3d\n')
    timefile.write('time,utc_time\n')

    for topic, msg, t in bag.read_messages():
        if(topic == '/gnss/fix'):
            fixfile.write(f"{t.to_nsec()},{msg.type},{msg.mode_selection},{msg.mode},{msg.satellite_count}\n")
        elif(topic == '/gnss/position'):
            posfile.write(f"{t.to_nsec()},{msg.latitude:0.8f},{msg.longitude:0.8f},{msg.altitude:0.8f},{msg.separation:0.8f},{msg.fix_3d}\n")
        elif(topic == '/gnss/time'):
            timefile.write(f"{t.to_nsec()},{msg.utc_time.to_nsec()}\n")
