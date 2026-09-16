#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from my_custom_interfaces.srv import SetLed
 
class BatteryNode(Node): 
    def __init__(self):
        super().__init__("battery") 
        self.client_ = self.create_client(SetLed, "set_led")

        self.counter = 1

        self.timer_ = self.create_timer(1.0, self.callback_led_panel)
        self.get_logger().info("Battery Node has started.")


    def led_state(self, battery_state):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the LED_Panel Server.....")

        request = SetLed.Request()
        request.battery_state = battery_state

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_led_state, request = request))

    #Callback function for creating a client
    def callback_led_state(self, future, request):
        response = future.result()
        self.get_logger().info("Response received: LED Status " + str(response.success))

    #Callback function for timer
    def callback_led_panel(self):
        self.get_logger().info("Time: " + str(self.counter) + " seconds")

        if self.counter == 4:
            self.led_state(True)
            self.get_logger().info("Battery is Low.")
        elif self.counter == 10:
            self.led_state(False)
            self.get_logger().info("Battery is Full.")
            self.counter = 0

        self.counter += 1

 
 
def main(args=None):
    rclpy.init(args=args)

    node = BatteryNode()

    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
