#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_multiply


class IMUConverter:
    def __init__(self):
        rospy.init_node('imu_converter', anonymous=True)
        
        # Subscribing to the VN100 IMU data topic
        self.imu_sub = rospy.Subscriber('/vn100/imu', Imu, self.imu_callback)
        
        # Publishing the adjusted 9DOF IMU data
        self.imu_9dof_pub = rospy.Publisher('/vn100/imu_9dof', Imu, queue_size=200)


    def imu_callback(self, msg):
        # Extract data from the incoming IMU message
        # linear_acceleration = msg.linear_acceleration
        # angular_velocity = msg.angular_velocity
        # orientation = msg.orientation

        # # Invert Z-axis and Y-axis values due to IMU mounting orientation
        # linear_acceleration.z = -linear_acceleration.z
        # linear_acceleration.y = -linear_acceleration.y
        # angular_velocity.z = -angular_velocity.z
        # angular_velocity.y = -angular_velocity.y
        
        # # Original quaternion from the IMU data
        # original_orientation = [orientation.x, orientation.y, orientation.z, orientation.w]

        # # Quaternion to multiply with (0, 0, 1, 0)
        # q2 = [0, 0, 1, 0]

        # # Perform quaternion multiplication
        # result_orientation = quaternion_multiply(original_orientation, q2)

        # Create new IMU message for 9-DOF
        imu_9dof_msg = Imu()
        imu_9dof_msg.header = msg.header
        # imu_9dof_msg.header.frame_id = 'body'

        # Populate IMU message fields
        imu_9dof_msg.linear_acceleration.x = msg.linear_acceleration.x
        imu_9dof_msg.linear_acceleration.y = -msg.linear_acceleration.y
        imu_9dof_msg.linear_acceleration.z = -msg.linear_acceleration.z
        
        imu_9dof_msg.angular_velocity.x = msg.angular_velocity.x
        imu_9dof_msg.angular_velocity.y = -msg.angular_velocity.y
        imu_9dof_msg.angular_velocity.z = -msg.angular_velocity.z

        imu_9dof_msg.orientation = Quaternion(*quaternion_multiply([msg.orientation.x,
                                                                    msg.orientation.y, 
                                                                    msg.orientation.z,
                                                                    msg.orientation.w],
                                                                    [0, 0, 1, 0]))
        
        # Publish the 9-DOF IMU message
        self.imu_9dof_pub.publish(imu_9dof_msg)


if __name__ == '__main__':
    try:
        IMUConverter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
