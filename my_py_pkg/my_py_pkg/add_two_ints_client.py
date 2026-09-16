#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial
 
class AddTwoIntsClient(Node): 
    def __init__(self):
        super().__init__("add_two_ints_client") 
        self.client_ = self.create_client(AddTwoInts, "add_two_ints")


    #Function that will receive & send  a & b value and waits if server is not up
    def call_add_two_ints(self, a, b):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the AddTwoInts Server.....")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_add_two_ints, request = request))

    #Callback function for creating a client
    def callback_call_add_two_ints(self, future, request):
        response = future.result()
        self.get_logger().info("Response received: " + str(request.a) + " + " + str(request.b) + " = " + str(response.sum))
 
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()

    for i in range(0, 15):
        node.call_add_two_ints(i,i*3)

    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
