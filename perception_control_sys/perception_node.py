#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        # Subscribe to camera image
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        
        # Publish the centroid of the detected object
        self.publisher_ = self.create_publisher(Point, '/target_position', 10)
        self.br = CvBridge()
        
        # Color detection bounds (e.g., detecting red)
        # Red can wrap around in HSV, so we define two ranges
        self.lower_red1 = np.array([0, 120, 70])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 120, 70])
        self.upper_red2 = np.array([180, 255, 255])

        self.get_logger().info('Perception node started. Looking for red objects...')

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            current_frame = self.br.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Convert BGR to HSV
        hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        # Create masks for red color
        mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)
        mask = mask1 + mask2

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Filter by area to ignore noise
            if cv2.contourArea(largest_contour) > 500:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    # Image dimensions
                    height, width, _ = current_frame.shape

                    # Normalize coordinates to range [-1.0, 1.0] relative to the center
                    # X: -1 (left) to 1 (right)
                    # Y: -1 (top) to 1 (bottom)
                    norm_x = (cX - width / 2) / (width / 2)
                    norm_y = (cY - height / 2) / (height / 2)

                    point_msg = Point()
                    point_msg.x = float(norm_x)
                    point_msg.y = float(norm_y)
                    point_msg.z = float(cv2.contourArea(largest_contour)) # Use Z for area/distance proxy
                    
                    self.publisher_.publish(point_msg)
                    self.get_logger().debug(f'Target detected at X: {norm_x:.2f}, Y: {norm_y:.2f}, Area: {point_msg.z}')

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
