#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

#Message type for the position topic
from turtlesim.msg import Pose
#Message type for the cmd_vel subscriber topic
from geometry_msgs.msg import Twist 

 
class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller") 

        self.pose : Pose = None

        # Creating a subscriber to the POS topic of the turtle to get the position of Turtle
        self.pos_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.callback_pos, 10)

        #Create a publisher to the cmd__vel topic to give command to the turtle to reach the target
        self.vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.control_loop_timer = self.create_timer(0.01, self.control_loop)
    
    def callback_pos(self, pose: Pose):
        self.pose = pose

    def control_loop(self):
        pass

    
 
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
