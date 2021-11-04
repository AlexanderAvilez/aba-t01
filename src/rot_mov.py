#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class RobotControl():

    def __init__(self):
        rospy.init_node('pubnode', anonymous=True)
        self.vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        rospy.on_shutdown(self.shutdownhook)

    def publish_once_in_cmd_vel(self):
        while not self.ctrl_c:
            connections = self.vel_publisher.get_num_connections()
            if connections > 0:
                self.vel_publisher.publish(self.cmd)
                break
            else:
                self.rate.sleep()

    def shutdownhook(self):
        self.stop_robot()
        self.ctrl_c = True

    def stop_robot(self):
        detener = raw_input('Escribar "Detener" para parar el robot: ')
        if(detener == "Detener"):
            rospy.loginfo("shutdown time! Stop the robot")
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
            self.publish_once_in_cmd_vel()

    def get_inputs_rotate(self):
        lectura_string = raw_input('Ingresa la entrada -> Avanzar / Girar : ')
        if lectura_string == "Girar":
            self.lineal_speed_x = 0
            clockwise_yn = raw_input('Quieres realizar el giro en sentido de las manecillas del reloj? (y/n): ')
            if clockwise_yn == "y":
                self.clockwise = True
            if clockwise_yn == "n":
                self.clockwise = False
            self.angular_speed_d = int(
                raw_input('Ingresa la velocidad angular (degrees): '))
            self.angle_d = int(raw_input('Ingresa el angulo (degrees): '))
        if lectura_string == "Avanzar":
            self.angular_speed_d = 0
            self.angle_d = 0
            self.clockwise = True
            self.lineal_speed_x = int(raw_input('Ingresa la velocidad lineal en x: '))
        return [self.angular_speed_d, self.angle_d,self.lineal_speed_x]

    def convert_degree_to_rad(self, speed_deg, angle_deg):
        self.angular_speed_r = speed_deg * 3.14 / 180
        self.angle_r = angle_deg * 3.14 / 180
        self.lineal_speed_r = 90
        return [self.angular_speed_r, self.angle_r]

    def rotate(self):
        self.cmd.linear.x = 0
        self.cmd.linear.y = 0
        self.cmd.linear.z = 0
        self.cmd.angular.x = 0
        self.cmd.angular.y = 0

        speed_d, angle_d, speed_x  = self.get_inputs_rotate()
        self.convert_degree_to_rad(speed_d, angle_d)

        if self.clockwise:
            self.cmd.angular.z = -abs(self.angular_speed_r)
        else:
            self.cmd.angular.z = abs(self.angular_speed_r)
        self.cmd.linear.x = speed_x
        rospy.loginfo(speed_x)

        t0 = rospy.Time.now().secs

        current_angle = 0

        while (current_angle < self.angle_r):

            self.vel_publisher.publish(self.cmd)
            t1 = rospy.Time.now().secs
            current_angle = self.angular_speed_r * (t1 - t0)
            self.rate.sleep()
        if(speed_x > 0):
            self.vel_publisher.publish(self.cmd)

if __name__ == '__main__':
    robotcontrol_object = RobotControl()
    try:
        res = robotcontrol_object.rotate()
    except rospy.ROSInterruptException:
        pass