# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from manus_ros2_msgs.msg import ManusGlove

from ah_wrapper import AHSerialClient
from ah_simulators.ah_mujoco import AHMujocoSim
import numpy as np
import random
import time

# Create serial client
client = AHSerialClient(simulated=True, write_thread=False)

# Initialize Mujoco simulator with the hand
# Ensure that AHSerialClient parameter simulated=True
# sim = AHMujocoSim(
#     hand=client.hand, 
#     scene=os.path.join(os.path.dirname(__file__), 'assets/psyonic_universal_robots_ur5e/scene.xml')  # Absolute path to assets
# )

class ManusSubscriber(Node):

    def __init__(self):
        super().__init__('manus_subscriber')
        self.subscription = self.create_subscription(
            ManusGlove,
            'manus_glove_0',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.fingers = [0 for _ in range(6)]

    def listener_callback(self, msg):

        for ergo_data in msg.ergonomics:
            # Scale MCP stretch values to [0, 100] based on individual finger ranges
            if ergo_data.type == "IndexMCPStretch":
                # MCP range: [5, 90]
                self.fingers[0] = max(0, min((ergo_data.value - 5) / 85 * 100, 100))
            elif ergo_data.type == "MiddleMCPStretch":
                # MCP range: [10, 85]
                self.fingers[1] = max(0, min((ergo_data.value - 10) / 75 * 100, 100))
            elif ergo_data.type == "RingMCPStretch":
                # MCP range: [10, 80]
                self.fingers[2] = max(0, min((ergo_data.value - 10) / 70 * 100, 100))
            elif ergo_data.type == "PinkyMCPStretch":
                # MCP range: [5, 70]
                self.fingers[3] = max(0, min((ergo_data.value - 5) / 65 * 100, 100))
            elif ergo_data.type == "ThumbMCPStretch":
                # MCP range: [-10, 60]
                self.fingers[4] = max(0, min(((ergo_data.value + 10) / 70) * 100, 100))
                self.fingers[4] -= 100
                self.fingers[4] *= -1
            elif ergo_data.type == "ThumbMCPSpread":
                # MCP range: [-5, 35]
                self.fingers[5] = max(0, min((ergo_data.value + 5) / 40 * 100, 100))
                self.fingers[5] *= -1

        # print(f"Fingers: {self.fingers}")
        client.set_position(self.fingers)
        client.send_command()


def main(args=None):
    rclpy.init(args=args)

    manus_subscriber = ManusSubscriber()

    rclpy.spin(manus_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    manus_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()