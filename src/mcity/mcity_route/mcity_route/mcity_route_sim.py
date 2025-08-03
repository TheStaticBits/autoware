#!/usr/bin/env python3

# Copyright 2022 Tier IV, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from tier4_system_msgs.srv import ChangeOperationMode, ChangeAutowareControl
from autoware_adapi_v1_msgs.srv import SetRoutePoints
from autoware_auto_system_msgs.msg import AutowareState


class McityRouteSim(Node):
    """
    Python implementation of the Autoware Interface Demo for Cosimulation.
    
    This node handles the interface between Autoware and the simulation environment,
    including localization initialization, route setting, and operation mode management.
    """

    def __init__(self):
        super().__init__('autoware_interface_demo_cosim')
        
        # Initialize state
        self.autoware_state = 1
        
        # Create publishers
        self.pub_local = self.create_publisher(
            PoseWithCovarianceStamped, 
            '/initialpose', 
            10
        )
        
        # Create subscriptions
        self.sub_autoware_state = self.create_subscription(
            AutowareState,
            '/autoware/state',
            self.autoware_state_callback,
            10
        )
        
        # Create service clients
        self.cli_set_route_points = self.create_client(
            SetRoutePoints,
            '/planning/mission_planning/set_route_points'
        )
        
        self.cli_set_operation_mode = self.create_client(
            ChangeOperationMode,
            '/system/operation_mode/change_operation_mode'
        )
        
        self.cli_set_autoware_control = self.create_client(
            ChangeAutowareControl,
            '/system/operation_mode/change_autoware_control'
        )
        
        # Create timer (1000ms = 1 second)
        self.timer = self.create_timer(1.0, self.on_timer)
        
        self.get_logger().info("McityRouteSim initialized")

    def on_timer(self):
        """Timer callback that handles different Autoware states."""
        if self.autoware_state == AutowareState.INITIALIZING:
            self.init_localization()
            self.get_logger().info("Waiting for vehicle initialization...")
        elif self.autoware_state == AutowareState.WAITING_FOR_ROUTE:
            self.set_route_points()
            self.get_logger().info("Setting route points...")
        elif self.autoware_state == AutowareState.WAITING_FOR_ENGAGE:
            self.set_autoware_control(True)
            self.set_operation_mode(ChangeOperationMode.Request.AUTONOMOUS)
            self.get_logger().info("Enabling autoware control...")

    def init_localization(self):
        """Initialize localization with the exact same coordinates as the C++ version."""
        localization_msg = PoseWithCovarianceStamped()
        
        localization_msg.pose.pose.position.x = 133.0123291015625
        localization_msg.pose.pose.position.y = 21.05602264404297
        localization_msg.pose.pose.position.z = 0.0
        
        localization_msg.pose.pose.orientation.x = 0.0
        localization_msg.pose.pose.orientation.y = 0.0
        localization_msg.pose.pose.orientation.z = 0.36693415416239533
        localization_msg.pose.pose.orientation.w = 0.9302469169576041
        
        # Set header
        localization_msg.header.stamp = self.get_clock().now().to_msg()
        localization_msg.header.frame_id = "map"
        
        # Publish
        self.pub_local.publish(localization_msg)

    def set_route_points(self):
        """Set route points with the exact same coordinates as the C++ version."""
        wp0 = Pose()
        wp0.position.x = 153.94821166992188
        wp0.position.y = 209.9748077392578
        wp0.position.z = 0.0
        wp0.orientation.x = 0.0
        wp0.orientation.y = 0.0
        wp0.orientation.z = 0.7040023080395935
        wp0.orientation.w = 0.7101976839408344

        wp1 = Pose()
        wp1.position.x = 200.9136505126953
        wp1.position.y = 332.71807861328125
        wp1.position.z = 0.0
        wp1.orientation.x = 0.0
        wp1.orientation.y = 0.0
        wp1.orientation.z = 0.1576494929852369
        wp1.orientation.w = 0.98749513282927

        wp2 = Pose()
        wp2.position.x = 50.181983947753906
        wp2.position.y = 164.53213500976562
        wp2.position.z = 0.0
        wp2.orientation.x = 0.0
        wp2.orientation.y = 0.0
        wp2.orientation.z = -0.7154038211799519
        wp2.orientation.w = 0.6987112226385972

        wp3 = Pose()
        wp3.position.x = 107.86299133300781
        wp3.position.y = 115.83384704589844
        wp3.position.z = 0.0
        wp3.orientation.x = 0.0
        wp3.orientation.y = 0.0
        wp3.orientation.z = -0.7211064990042112
        wp3.orientation.w = 0.6928242324672901

        wp4 = Pose()
        wp4.position.x = 48.770851135253906
        wp4.position.y = 0.559809684753418
        wp4.position.z = 0.0
        wp4.orientation.x = 0.0
        wp4.orientation.y = 0.0
        wp4.orientation.z = 0.06425407328302392
        wp4.orientation.w = 0.9979335719708701

        # Wait for service
        while not self.cli_set_route_points.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error("Interrupted while waiting for the service. Exiting.")
                return
            self.get_logger().info("routing service not available, waiting again...")

        # Create request
        request = SetRoutePoints.Request()
        request.header.frame_id = "map"
        request.goal = wp4
        request.waypoints = [wp0, wp1, wp2, wp3]

        # Send request
        future = self.cli_set_route_points.call_async(request)
        self.get_logger().info("Setting new route...")

    def set_operation_mode(self, mode):
        """Set operation mode."""
        request = ChangeOperationMode.Request()
        request.mode = mode

        while not self.cli_set_operation_mode.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error("Interrupted while waiting for the service. Exiting.")
                return
            self.get_logger().info("operation mode service not available, waiting again...")

        future = self.cli_set_operation_mode.call_async(request)

    def set_autoware_control(self, autoware_control):
        """Set autoware control."""
        request = ChangeAutowareControl.Request()
        request.autoware_control = autoware_control

        while not self.cli_set_autoware_control.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error("Interrupted while waiting for the service. Exiting.")
                return
            self.get_logger().info("autoware control service not available, waiting again...")

        future = self.cli_set_autoware_control.call_async(request)

    def autoware_state_callback(self, msg):
        """Callback for autoware state updates."""
        self.autoware_state = msg.state


def main(args=None):
    rclpy.init(args=args)
    
    node = McityRouteSim()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 