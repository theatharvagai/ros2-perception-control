from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception_control_sys',
            executable='perception_node',
            name='perception_node',
            output='screen'
        ),
        Node(
            package='perception_control_sys',
            executable='control_node',
            name='control_node',
            output='screen'
        ),
        Node(
            package='perception_control_sys',
            executable='telemetry_node',
            name='telemetry_node',
            output='screen'
        )
    ])