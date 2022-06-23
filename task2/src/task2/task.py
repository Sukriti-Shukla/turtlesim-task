#!/usr/bin/env python
# import necesary modules
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty
from turtlesim.srv import *
import time

c=3
class Turtle:
    
    def __init__(self, i,x,y,vx,vy):
        # Node initialised
        self.name = 'turtle' + str(i)
        
        serv = rospy.ServiceProxy('/spawn', Spawn)
        serv(x, y, 0, self.name)
        self.velocity_publisher = rospy.Publisher('/' + self.name + '/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(100)
        self.v_msg = Twist()
        self.v_msg.linear.x = vx
        self.v_msg.linear.y = vy
        self.velocity_publisher.publish(self.v_msg)
    def newTurtle(self):
        self.velocity_subscriber= rospy.Subscriber('/' + self.name + '/pose', Pose, self.update_pose)
        self.velocity_publisher.publish(self.v_msg)
   #self.pose=Pose()
    # function to update own postion
    def update_pose(self, data):
        global c
        self.velocity_publisher.publish(self.v_msg)
        
        if (data.x<=1) or (data.x>=8):
            c+=1
            self.v_msg.linear.x*=-1
            self.velocity_publisher.publish(self.v_msg)
            v1 = self.v_msg.linear.x
            v2 = -1*self.v_msg.linear.y

            if(data.x<1):
               pos1 = data.x+0.1
            else:
               pos1 = data.x-0.1
            pos2=data.y
            if (c<16):
               tut = Turtle(c,pos1,pos2,v1,v2)
               tut.newTurtle()
        
        if (data.y<=1) or (data.y>=8):
            c+=1
            self.v_msg.linear.y*=-1
            self.velocity_publisher.publish(self.v_msg)
            v1 = -1*self.v_msg.linear.x
            v2 = self.v_msg.linear.y
            if(data.y<1):
               pos2 = data.y+0.1
            else:
               pos2 = data.y-0.1
            pos1=data.x
            if(c<16):
               tut = Turtle(c,pos1,pos2,v1,v2)
               tut.newTurtle()

rospy.init_node('Turtle')
for i in range(1):
    ob = Turtle(2,2,2,3,5)
    ob.newTurtle()
    break
rospy.spin()

        # Publish at the desired rate.
       # self.rate.sleep()        
# if __name__ == '__main__':
#     try:
#         x = turtle1()
#         x.move()
#     except rospy.ROSInterruptException:
#         pass