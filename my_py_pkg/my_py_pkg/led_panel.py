#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from my_custom_interfaces.srv import SetLed
from my_custom_interfaces.msg import LedPanelState
 
 
class LedPanelNode(Node): 
    def __init__(self):
        super().__init__("led_panel_node")

        self.led_status = [0,0,0]

        #Creating the Server that will accept the request
        self.server_ = self.create_service(SetLed, "set_led", self.callback_led_panel)

        self.publisher_ = self.create_publisher(LedPanelState, "led_panel_state", 10)

        self.timer_ = self.create_timer(1.0, self.callback_publisher)

        self.get_logger().info("LED Server has started....")

    #Defining the callback function for Server
    def callback_led_panel (self, request: SetLed.Request, response: SetLed.Response):

        if request.battery_state:
            response.success = True
            self.led_status = [0,0,1]
            self.get_logger().info("LED Turned On")

        elif not request.battery_state:
            response.success = False
            self.led_status = [0,0,0]
            self.get_logger().info("LED Turned Off")

        return response

    def callback_publisher(self):
        msg = LedPanelState()
        msg.led_state = self.led_status
        self.publisher_.publish(msg)

 
 
def main(args=None):
    rclpy.init(args=args)

    node = LedPanelNode() 

    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
