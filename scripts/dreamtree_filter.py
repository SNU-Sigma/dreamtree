#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
from scipy import signal

sample_num = 10
fir_seq = signal.firwin(sample_num, 0.2, nyq=50)
signal_seq = []
signal_filtered_pub = rospy.Publisher("/signal_filtered", Int16, queue_size=100)

data_seq = []
thumb_data_seq = []
fore_finger_data_seq = []
middle_finger_data_seq = []
ring_finger_data_seq = []

publishers = []
thumb_filtered_pub = rospy.Publisher("/dreamtree/thumb/filtered", Int16, queue_size=100)
fore_finger_filtered_pub = rospy.Publisher("/dreamtree/fore_finger/filtered", Int16, queue_size=100)
middle_finger_filtered_pub = rospy.Publisher("/dreamtree/middle_finger/filtered", Int16, queue_size=100)
ring_finger_filtered_pub = rospy.Publisher("/dreamtree/ring_finger/filtered", Int16, queue_size=100)


def signal_callback(data, index):
    # rospy.loginfo(signal_seq)
    # signal_seq.append(data.data)
    # if signal_seq.__len__() == sample_num :
    #     rospy.loginfo("ok")
    #     signal_filtered_pub.publish(signal.convolve(signal_seq, fir_seq, 'same')[2])
    #     signal_seq.pop(0)
    data_seq[index].append(data)
    if data_seq[index].__len__() == sample_num :
        publishers[index].publish(signal.convolve(data_seq[index], fir_seq, 'same')[2])
        data_seq[index].pop(0)


def thumb_callback(msg):
    rospy.loginfo("ddd")
    signal_callback(msg.data, 0)


def fore_finger_callback(msg):
    signal_callback(msg.data, 1)


def middle_finger_callback(msg):
    signal_callback(msg.data, 2)


def ring_finger_callback(msg):
    signal_callback(msg.data, 3)


if __name__=='__main__':
    rospy.init_node("hand_recognizer", anonymous=True)
    global hand_num
    hand_num = rospy.get_param('~hand_num', 1)
    global hand_dir

    hand_dir = rospy.get_param('~hand_dir', "right")
    rospy.Subscriber("/dreamtree/thumb/raw", Int16, thumb_callback)
    rospy.Subscriber("/dreamtree/fore_finger/raw", Int16, fore_finger_callback)
    rospy.Subscriber("/dreamtree/middle_finger/raw", Int16, middle_finger_callback)
    rospy.Subscriber("/dreamtree/ring_finger/raw", Int16, ring_finger_callback)

    publishers.append(thumb_filtered_pub)
    publishers.append(fore_finger_filtered_pub)
    publishers.append(middle_finger_filtered_pub)
    publishers.append(ring_finger_filtered_pub)

    data_seq.append(thumb_data_seq)
    data_seq.append(fore_finger_data_seq)
    data_seq.append(middle_finger_data_seq)
    data_seq.append(ring_finger_data_seq)

    rospy.loginfo("ddd")
    rospy.spin()