#!/bin/python

# from importRosbag.importRosbag import importRosbag

# topics = importRosbag(filePathOrName='_2020-06-09-15-08-36_0.bag')
# print(topics)

#pip install pycryptodome
#pip install pycryptodomex
#pip install gnupg
#pip install rospkg
#pip install lz4

import struct
import sys
import time

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import rosbag

from rosbag.bag import BagMessage

import numpy as np

def doWork(infile, maxcloud = -1):
    # infile = '_2020-06-09-15-08-36_0.bag'

    bg = rosbag.Bag(infile)
    print(bg.get_message_count())
    print(bg.get_compression_info())
    # msgs = bg.read_messages()

    msgs = bg.read_messages(topics=['/livox/lidar'])


    # _sensor_msgs__PointCloud2

    outf = open(infile+".lid","wb+")
    i = 0
    
    # a point time
    dt = 0.05 / 12000 # horizon
    # dt = 0.1 / 10000 # mid40
    # over

    for msg in msgs:
        # topics.add(msg.topic)
        # if msg.topic != "/livox/lidar":
        #     continue
        # print(msg.message)
        # print(type(msg))
        if(i%5 == 0):
            print i
        i += 1
        if( maxcloud > 0 and i > maxcloud):
            break
        # print(type(msg.message))
        # print(msg.message.__slots__)
        # print (msg.message.row_step)
        # print (type(msg.message.data))
        # print (type(msg.message.fields))
        # print (type(msg.message.height))


        ''' 
        save file with bin format: every unit use
            32*4 +64 = 192 bytes
        struct APOINT
        {
        float x;
        float y;
        float z;
        float rfl;
        double t;
        };
        '''

        # print("{:.6f}".format(msg.timestamp.to_time()))

        outbuf = ""
        points = point_cloud2.read_points(msg.message, field_names=("x", "y", "z", "intensity"), skip_nans=True)

        count = 0

        for point in points:
            # outdata = struct.pack("ffffd", float(point[0]), 
            #     float(point[1]), float(point[2]), float(point[3]), 
            #     float(msg.timestamp.to_time()))
            outdata = struct.pack("ffffd", float(point[0]), 
                float(point[1]), float(point[2]), float(point[3]), 
                float(msg.timestamp.to_time() + count*dt))
            count = count + 1
            outbuf += outdata
            if(len(outbuf) > 1024*1024):
                outf.write(outbuf)
                outbuf = ""
            # outf.write(outdata)
            # print msg.timestamp, point[0]  #print x
        if(len(outbuf) > 0):
            outf.write(outbuf)
        # break

    outf.close()
    # print topics


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "Usage:"+sys.argv[0]+" inbagfile maxprocessclound"
        exit(0)
    pretime = time.time()
    maxcld = -1
    if(len(sys.argv) > 2):
        maxcld = int(sys.argv[2])
    doWork(sys.argv[1], maxcld)
    print "seconds:%d"%(time.time() - pretime)
