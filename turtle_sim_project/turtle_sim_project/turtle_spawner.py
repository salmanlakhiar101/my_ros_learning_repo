#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import math
import random
from functools import partial

#Message type for the Service
from turtlesim.srv import Spawn
#Custom Interface import
from my_custom_interfaces.msg import Turtle
from my_custom_interfaces.msg import TurtleArray
 
 
class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        #Veriables etc
        self.turtle_name_prefix = "Turtle"
        self.counter = 1
        self.alive_turtles = []

        #Publisher, Services etc
        self.alive_turtles_publisher = self.create_publisher(TurtleArray, "alive_turtles", 10)
        self.spawn_client = self.create_client(Spawn, "/spawn")
        self.spawn_timer = self.create_timer(3.0, self.spawn_new_turtle)


    #Publishing the alive turtles
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtle = self.alive_turtles
        self.alive_turtles_publisher.publish(msg)


    #This function will call the call_spawn_service function and uses this function to generate random turtles
    def spawn_new_turtle(self):
        self.counter +=1
        name = self.turtle_name_prefix + str(self.counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi) #2*pi will cover full 360`

        self.call_spawn_service(name, x, y, theta)

    #This is the function that will generate a turtle and handles service functions
    def call_spawn_service(self, turtle_name, x, y, theta):
        while not self.spawn_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the Spawn service...")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = self.spawn_client.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn_service, request = request))

    def callback_call_spawn_service(self, future, request: Spawn.Request):
        response : Spawn.Response = future.result()

        if response.name != "":
            self.get_logger().info("New Alive Turtle " + response.name)

            new_turtle = Turtle()
            
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta

            self.alive_turtles.append(new_turtle)

            self.publish_alive_turtles()


        

 
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    #node.call_spawn_service("Turtle2", 1.0, 2.0, 0.0)

    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
