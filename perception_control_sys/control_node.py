#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')
        
        # Subscribe to target position published by perception node
        self.subscription = self.create_subscription(
            Point,
            '/target_position',
            self.target_callback,
            10)
            
        # Publisher for robot velocity
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # PID Constants
        self.Kp_angular = 1.0
        self.Kp_linear = 0.5
        
        # Target area representing "close enough"
        self.target_area = 50000.0 
        
        self.get_logger().info('Control node started. Waiting for target...')

    def target_callback(self, msg):
        target_x = msg.x
        target_area = msg.z
        
        vel_msg = Twist()
        
        # Proportional control for angular velocity (turning towards object)
        # target_x is normalized [-1, 1], where 0 is centered.
        # If target_x > 0 (object is to the right), turn right (negative angular.z)
        vel_msg.angular.z = -self.Kp_angular * target_x
        
        # Proportional control for linear velocity (moving towards object)
        # Move forward if object is detected. Slow down as it gets closer (larger area).
        area_error = self.target_area - target_area
        
        if area_error > 0:
            # The smaller the area (farther away), the faster we move
            # Normalize area error based on target_area
            linear_speed = self.Kp_linear * (area_error / self.target_area)
            # Cap the maximum linear speed
            vel_msg.linear.x = min(linear_speed, 0.5)
        else:
            # Reached target or too close
            vel_msg.linear.x = 0.0
            
        self.publisher_.publish(vel_msg)
        self.get_logger().debug(f'Publishing Cmd Vel - Linear: {vel_msg.linear.x:.2f}, Angular: {vel_msg.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot before shutting down
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
