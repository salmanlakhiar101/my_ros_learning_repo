#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64 
 
class NumberCounter(Node): 
    def __init__(self):
        super().__init__("number_counter")
        self.even_number = 0

        self.subscriber_ = self.create_subscription(Int64, "number", self.callback_robot_news, 10) 
        self.get_logger().info("Number Counter Node has been Created!")

        self.publisher_ = self.create_publisher(Int64, "number_counter", 10)
        self.timer_ = self.create_timer(1, self.publish_news)


    def callback_robot_news(self, msg:Int64):
        if msg.data%2 == 0:
            self.get_logger().info(str(msg.data) + " is a Even Number")
            self.even_number = msg.data
        else:
            self.get_logger().info(str(msg.data) + " is a Odd Number")

    def publish_news(self):
        new_msg = Int64()
        new_msg.data = self.even_number
        self.publisher_.publish(new_msg)


 
 
def main(args=None):
   rclpy.init(args=args)
   node = NumberCounter() 
   rclpy.spin(node)
   rclpy.shutdown()
 
 
if __name__ == "__main__":
   main()
