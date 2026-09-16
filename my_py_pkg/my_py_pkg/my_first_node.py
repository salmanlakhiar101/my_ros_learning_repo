#!/usr/bin/env python3


#Importing Libraries
import rclpy
from rclpy.node import Node


#Creating Node Class
class MyNode(Node):

    def __init__(self):
        #Initializing parent class constructor with node name "py_test" 
        super().__init__("py_test")

        #Counter veriable
        self.counter = 0

        self.get_logger().info("Hello ROS World!")

        #Creating a timer
        self.create_timer(1.0, self.timer_callback)

        

    #Creating Timer Function
    def timer_callback(self):
        self.get_logger().info("Hello {}".format(self.counter))
        self.counter += 1



def main(args = None):

    #Initiating node
    rclpy.init(args = args)

    #Creating an instance of node class
    node = MyNode()

    #To keep the node alive
    rclpy.spin(node)

    #Shutting the node
    rclpy.shutdown()


if __name__ == "__main__":
    main()
