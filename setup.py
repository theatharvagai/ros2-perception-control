from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'perception_control_sys'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools', 'opencv-python', 'numpy'],
    zip_safe=True,
    maintainer='Robotics Engineer',
    maintainer_email='contact@example.com',
    description='ROS2-Based Perception & Control System for Autonomous Manipulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'perception_node = perception_control_sys.perception_node:main',
            'control_node = perception_control_sys.control_node:main',
            'telemetry_node = perception_control_sys.telemetry_node:main',
        ],
    },
)