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

from geometry_msgs.msg import Pose
from mcity_msgs.msg import VehicleState
from autoware_adapi_v1_msgs.srv import SetRoutePoints
from autoware_adapi_v1_msgs.msg import OperationModeState
from tier4_system_msgs.srv import ChangeOperationMode, ChangeAutowareControl
from autoware_auto_system_msgs.msg import AutowareState


class McityRouteRealcar(Node):
    """
    Python implementation of the Autoware Interface Demo for Real Car.
    
    This node handles the interface between Autoware and the real vehicle,
    including vehicle state monitoring, route setting, and operation mode management.
    """

    def __init__(self):
        super().__init__('autoware_interface_demo_realcar')
        
        # Initialize state
        self.autoware_state = 1
        
        self.STEER_TO_TIRE_RATIO = 16.0
        
        # Initialize vehicle state message
        self.veh_state_msg = VehicleState()
        
        # Initialize operation mode state message
        self.operation_mode_state_msg = OperationModeState()
        
        # Create subscriptions
        self.sub_autoware_state = self.create_subscription(
            AutowareState,
            '/autoware/state',
            self.autoware_state_callback,
            10,
        )

        self.sub_operation_mode = self.create_subscription(
            OperationModeState,
            '/system/operation_mode/state',
            self.operation_mode_state_callback,
            10,
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
        
        # Create timer (100ms = 0.1 second)
        self.timer = self.create_timer(0.1, self.on_timer)
        
        self.get_logger().info("McityRouteRealcar initialized")

    def on_timer(self):
        """Timer callback that handles different Autoware states and vehicle reporting."""
        if self.autoware_state == AutowareState.INITIALIZING:
            self.get_logger().info("Waiting for vehicle initialization...")
            return
        elif self.autoware_state == AutowareState.WAITING_FOR_ROUTE:
            self.set_route_points()
            self.operation_mode_state_msg.mode = ChangeOperationMode.Request.LOCAL
            self.get_logger().info("Setting route points...")
        else:
            # Handle operation mode based on vehicle state
            if (not self.veh_state_msg.by_wire_enabled and 
                self.veh_state_msg.speed_x < 0.25 and 
                int(self.operation_mode_state_msg.mode) != ChangeOperationMode.Request.STOP):
                self.set_operation_mode(ChangeOperationMode.Request.STOP)
            elif (not self.veh_state_msg.by_wire_enabled and 
                  self.veh_state_msg.speed_x >= 0.25 and 
                  int(self.operation_mode_state_msg.mode) != ChangeOperationMode.Request.LOCAL):
                self.set_operation_mode(ChangeOperationMode.Request.LOCAL)
            elif (self.veh_state_msg.by_wire_enabled and 
                  int(self.operation_mode_state_msg.mode) != ChangeOperationMode.Request.AUTONOMOUS):
                self.set_operation_mode(ChangeOperationMode.Request.AUTONOMOUS)

    def set_route_points(self):
        """Set route points with the exact same coordinates as the C++ version."""
        wp0 = Pose()
        wp0.position.x = 159.460693359375
        wp0.position.y = 256.66790771484375
        wp0.position.z = 0.0
        wp0.orientation.x = 0.0
        wp0.orientation.y = 0.0
        wp0.orientation.z = 0.6955498525464231
        wp0.orientation.w = 0.718477837252235

        wp1 = Pose()
        wp1.position.x = 196.44869995117188
        wp1.position.y = 326.031494140625
        wp1.position.z = 0.0
        wp1.orientation.x = 0.0
        wp1.orientation.y = 0.0
        wp1.orientation.z = 0.10959365387983362
        wp1.orientation.w = 0.9939764740823935

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

    def operation_mode_state_callback(self, msg):
        """Callback for operation mode state updates."""
        self.operation_mode_state_msg = msg


def main(args=None):
    rclpy.init(args=args)
    
    node = McityRouteRealcar()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 