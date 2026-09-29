#!/usr/bin/env python3

#ROS libraries
import rclpy
from rclpy.node import Node

import math
from functools import partial

#Message type for the position topic
from turtlesim.msg import Pose
#Message type for the cmd_vel subscriber topic
from geometry_msgs.msg import Twist 
#Custom Interface import
from my_custom_interfaces.msg import Turtle
from my_custom_interfaces.msg import TurtleArray
from my_custom_interfaces.srv import CatchTurtle

 
class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller") 

        #The target Position for the turtle
        self.turtle_to_catch = None
        self.pose : Pose = None
        
        self.declare_parameter("closest_turtle_catch", True)
        self.closest_turtle_catch = self.get_parameter("closest_turtle_catch").value

        # Creating a subscriber to the POS topic of the turtle to get the position of Turtle
        self.pos_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.callback_pos, 10)
        #Subscriber for the new alive turtles
        self.alive_turtles_sub = self.create_subscription(TurtleArray, "alive_turtles", self.call_back_alive_turtle, 10)

        #Create a publisher to the cmd__vel topic to give command to the turtle to reach the target
        self.vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        #Creating catch turtle Client to call Service from Spawn node to kill the turtle
        self.catch_turtle_client = self.create_client(CatchTurtle, "catch_turtle")

        #Timer for the control function
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)


    def call_back_alive_turtle(self, turtle_list: TurtleArray):
        if len(turtle_list.turtle) > 0:
            if self.closest_turtle_catch:
                closest_turtle = None
                distance_closest_turtle = None

                for turtle in turtle_list.turtle:
                    dist_x = turtle.x - self.pose.x
                    dist_y = turtle.y - self.pose.y

                    distance = math.sqrt((dist_x**2)+(dist_y**2))

                    if distance_closest_turtle == None or distance < distance_closest_turtle:
                        closest_turtle = turtle
                        distance_closest_turtle = distance

                self.turtle_to_catch = closest_turtle
                
            else:
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
            msg.linear.x = 3*distance

            target_theta = math.atan2(dist_y, dist_x)
            difference = target_theta - self.pose.theta

            #Normalizing the angle
            if difference > math.pi:
                difference -= 2*math.pi
            elif difference < -math.pi:
                difference += 2*math.pi

            msg.angular.z = 6*difference

        else:
            #Target reached, Robot is stopped.
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.call_catch_turtle_service(self.turtle_to_catch.name)
            self.turtle_to_catch = None

        
        self.vel_publisher.publish(msg)

    def call_catch_turtle_service(self, turtle_name):
        while not self.catch_turtle_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the Catch Turtle Service...")

        request = CatchTurtle.Request()
        request.name = turtle_name

        future = self.catch_turtle_client.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle_service, turtle_name = turtle_name))

    def callback_call_catch_turtle_service(self, future, turtle_name):
        response: CatchTurtle.Response = future.result()
        if not response.success:
            self.get_logger().error("Turtle " + turtle_name + " could'nt be removed.")


    
 
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
