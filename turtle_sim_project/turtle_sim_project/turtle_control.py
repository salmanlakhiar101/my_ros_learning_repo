#!/usr/bin/env python3
import math
#ROS libraries
import rclpy
from rclpy.node import Node

#Message type for the position topic
from turtlesim.msg import Pose
#Message type for the cmd_vel subscriber topic
from geometry_msgs.msg import Twist 
#Custom Interface import
from my_custom_interfaces.msg import Turtle
from my_custom_interfaces.msg import TurtleArray

 
class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller") 

        #The target Position for the turtle
        self.turtle_to_catch = None
        self.pose : Pose = None

        # Creating a subscriber to the POS topic of the turtle to get the position of Turtle
        self.pos_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.callback_pos, 10)

        #Create a publisher to the cmd__vel topic to give command to the turtle to reach the target
        self.vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        #Subscriber for the new alive turtles
        self.alive_turtles_sub = self.create_subscription(TurtleArray, "alive_turtles", self.call_back_alive_turtle, 10)

        #Timer for the control function
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)


    def call_back_alive_turtle(self, turtle_list: TurtleArray):
        if len(turtle_list.turtle) > 0:
            self.turtle_to_catch: Turtle = turtle_list.turtle[0]
    
    def callback_pos(self, pose: Pose):
        self.pose = pose

    def control_loop(self):

        #If in the begining the or can't get the position value of Turtle the code must not go to the distance computing stage.
        if self.pose == None or self.turtle_to_catch == None:
            return

        #Computing the distance
        dist_x = self.turtle_to_catch.x - self.pose.x
        dist_y = self.turtle_to_catch.y - self.pose.y

        #Calculating the hypotnese from base and perpendicular
        distance = math.sqrt((dist_x**2)+(dist_y**2))

        #Now publishing the data stage
        msg = Twist()

        if distance > 0.5:
            #Target hasn't reached
            
            #A P-Controller that will go with the velocity of "distance"
            msg.linear.x = 2*distance

            target_theta = math.atan2(dist_y, dist_x)
            difference = target_theta - self.pose.theta

            #Normalizing the angle
            if difference > math.pi:
                difference -= 2*math.pi
            elif difference < -math.pi:
                difference += 2*math.pi

            msg.angular.z = 3*difference

        else:
            #Target reached, Robot is stopped.
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        
        self.vel_publisher.publish(msg)
    
 
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
