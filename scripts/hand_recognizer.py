#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
from scipy import signal

sample_num = 10
fir_seq = signal.firwin(sample_num, 0.3, nyq=50)
signal_seq = []
signal_filtered_pub = rospy.Publisher("/signal_filtered", Int16, queue_size=100)
def signal_callback(data):
    rospy.loginfo(signal_seq)
    signal_seq.append(data.data)
    if signal_seq.__len__() == sample_num :
        rospy.loginfo("ok")
        signal_filtered_pub.publish(signal.convolve(signal_seq, fir_seq, 'same')[2])
        signal_seq.pop(0)

if __name__=='__main__':
    rospy.init_node("hand_recognizer", anonymous=True)
    global hand_num
    hand_num = rospy.get_param('~hand_num', 1)
    global hand_dir
    hand_dir = rospy.get_param('~hand_dir', "right")
    rospy.Subscriber("/signal", Int16, signal_callback)
    rospy.spin()