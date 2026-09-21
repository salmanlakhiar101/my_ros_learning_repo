#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math

#Message type for the position topic
from turtlesim.msg import Pose
#Message type for the cmd_vel subscriber topic
from geometry_msgs.msg import Twist 

 
class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller") 

        #The target Position for the turtle
        self.target_x = 8
        self.target_y = 2

        self.pose : Pose = None

        # Creating a subscriber to the POS topic of the turtle to get the position of Turtle
        self.pos_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.callback_pos, 10)

        #Create a publisher to the cmd__vel topic to give command to the turtle to reach the target
        self.vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.control_loop_timer = self.create_timer(0.01, self.control_loop)
    
    def callback_pos(self, pose: Pose):
        self.pose = pose

    def control_loop(self):

        #If in the begining the or can't get the position value of Turtle the code must not go to the distance computing stage.
        if self.pose == None:
            return

        #Computing the distance
        dist_x = self.target_x - self.pose.x
        dist_y = self.target_y - self.pose.y

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
