#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
import csv
import time
import os

class TelemetryNode(Node):
    def __init__(self):
        super().__init__('telemetry_node')
        
        self.target_sub = self.create_subscription(
            Point,
            '/target_position',
            self.target_callback,
            10)
            
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10)
            
        # Variables to store the latest data
        self.latest_target = None
        self.latest_cmd = None
        
        # Setup CSV Logging
        # Save to home directory or current execution dir
        self.log_file_path = os.path.join(os.getcwd(), 'telemetry_log.csv')
        self.csv_file = open(self.log_file_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Target_X', 'Target_Y', 'Target_Area', 'Cmd_Linear_X', 'Cmd_Angular_Z'])
        
        # Timer to log data at a fixed rate (e.g., 10 Hz)
        self.timer = self.create_timer(0.1, self.log_data)
        
        self.get_logger().info(f'Telemetry node started. Logging to {self.log_file_path}')

    def target_callback(self, msg):
        self.latest_target = msg

    def cmd_callback(self, msg):
        self.latest_cmd = msg
        
    def log_data(self):
        if self.latest_target and self.latest_cmd:
            timestamp = time.time()
            self.csv_writer.writerow([
                f"{timestamp:.3f}",
                f"{self.latest_target.x:.4f}",
                f"{self.latest_target.y:.4f}",
                f"{self.latest_target.z:.1f}",
                f"{self.latest_cmd.linear.x:.4f}",
                f"{self.latest_cmd.angular.z:.4f}"
            ])
            # Force write to disk occasionally or just rely on flush on exit,
            # but flushing ensures data is there if it crashes
            self.csv_file.flush()

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.csv_file.close()
        node.get_logger().info('Telemetry file closed.')
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
