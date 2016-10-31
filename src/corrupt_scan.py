#!/usr/bin/env python

import rospy
#import roslib; roslib.load_manifest('arf_logic')
from sensor_msgs.msg import LaserScan
from math import fmod
from numpy import random
import numpy as np

dyn_corruption = 0
pub = 0

def callback(data):
  #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.header.stamp)

  if dyn_corruption:
    scan_len = len(data.ranges);

    corr_samples = random.randint(0, high=scan_len-1,\
      size=int(round(scan_len*dyn_corruption/100)))
    noise_vec = random.rand(corr_samples.size)
    np_ranges = np.array(data.ranges)

    for i in range(corr_samples.size):
      np_ranges[corr_samples[i]] = \
        data.ranges[corr_samples[i]]*(1 - noise_vec[i])

    data.ranges = tuple(np_ranges)
  pub.publish(data)

def listener():
  global dyn_corruption, pub

  rospy.init_node('corrupt_scan', anonymous=True)

  rospy.Subscriber("/base_scan_1", LaserScan, callback)

  dyn_corruption = rospy.get_param('~dyn_corruption', 0)
  pub = rospy.Publisher('/scan', LaserScan, queue_size=100)

  rospy.loginfo("Corrupting data at %d", dyn_corruption)
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass

