# ROS2-Based Perception & Control System for Autonomous Manipulation (Simulation)

## 🧠 Project Overview
This project simulates a robot that detects an object (perception), plans its motion (basic logic), moves towards it (control), and logs performance (systems thinking). It demonstrates hands-on engineering skills required for modern robotics roles, specifically integrating ROS2, Perception, Control Systems, and Simulation.

## 🧩 System Architecture
The system is built as a modular ROS2 package (`perception_control_sys`) containing three main nodes:

1. **Perception Node (`perception_node.py`)**:
    - Subscribes to `/camera/image_raw`.
    - Uses OpenCV (`cv_bridge`) to detect a colored object (e.g., red ball) in the image stream.
    - Publishes the object's normalized centroid position and area to `/target_position`.

2. **Control Node (`control_node.py`)**:
    - Subscribes to `/target_position`.
    - Implements a Proportional-Integral-Derivative (PID) style proportional controller.
    - Publishes velocity commands (`geometry_msgs/Twist`) to `/cmd_vel` to align the robot and move it towards the detected object.

3. **Telemetry Logger (`telemetry_node.py`)**:
    - Subscribes to `/target_position` and `/cmd_vel`.
    - Logs latency, distance error (inferred by area), and control response into a `telemetry_log.csv` file for performance analysis.

## ⚙️ Tech Stack
- ROS2 (Humble/Iron)
- Python 3
- OpenCV
- Gazebo (Simulation Environment)
- RViz (Visualization)
- NumPy

## 📁 Repository Structure
```
ros2_ws/
 └── src/
     └── perception_control_sys/
         ├── launch/
         │   └── system_launch.py
         ├── perception_control_sys/
         │   ├── __init__.py
         │   ├── perception_node.py
         │   ├── control_node.py
         │   └── telemetry_node.py
         ├── package.xml
         └── setup.py
```

## 🛠️ Setup & Execution Instructions

### 1. Build the Workspace
Ensure you have ROS2 installed and sourced.
```bash
cd ros2_ws
colcon build
source install/setup.bash
```

### 2. Run the System Simulation
This project requires a simulated robot with a camera, such as a TurtleBot3 in a Gazebo world.
*Assuming you have TurtleBot3 Gazebo packages installed:*

**Terminal 1 (Simulation):**
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo empty_world.launch.py
```
*(You will need to manually spawn a red object, e.g., a colored sphere, in front of the robot in Gazebo).*

**Terminal 2 (Perception & Control Nodes):**
```bash
cd ros2_ws
source install/setup.bash
ros2 launch perception_control_sys system_launch.py
```

### 3. Output
- **Gazebo**: The robot should align its camera with the red object and drive towards it.
- **Terminal**: Logs indicating object detection coordinates and published velocity commands.
- **Logs**: A `telemetry_log.csv` file will be generated in the directory where the nodes were launched.

## 🧾 Resume Integration
**ROS2-Based Perception & Control System (Simulation)** — *Developed a modular robotics system using ROS2 integrating perception, control, and simulation; implemented real-time object detection and PID-based motion control in Gazebo with RViz visualization, enabling robust system integration, debugging, and performance logging.*