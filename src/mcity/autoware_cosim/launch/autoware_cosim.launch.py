#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare launch arguments
    control_cav_arg = DeclareLaunchArgument(
        'control_cav',
        default_value='false',
        description='Whether to control CAV from Autoware or Cosim'
    )
    
    cosim_controlled_vehicle_keys_arg = DeclareLaunchArgument(
        'cosim_controlled_vehicle_keys',
        default_value='[TERASIM_ACTOR_INFO]',
        description='List of cosim controlled vehicle keys'
    )

    # Get launch configuration
    control_cav = LaunchConfiguration('control_cav')
    cosim_controlled_vehicle_keys = LaunchConfiguration('cosim_controlled_vehicle_keys')

    # Create nodes for all executables
    autoware_vehicle_plugin_node = Node(
        package='autoware_cosim',
        executable='autoware_vehicle_plugin',
        name='autoware_vehicle_plugin',
        output='screen',
        parameters=[{
            'control_cav': control_cav,
            'cosim_controlled_vehicle_keys': cosim_controlled_vehicle_keys,
        }]
    )

    autoware_vehicle_report_node = Node(
        package='autoware_cosim',
        executable='autoware_vehicle_report',
        name='autoware_vehicle_report',
        output='screen'
    )

    autoware_tls_plugin_node = Node(
        package='autoware_cosim',
        executable='autoware_tls_plugin',
        name='autoware_tls_plugin',
        output='screen'
    )

    autoware_dummy_grid_node = Node(
        package='autoware_cosim',
        executable='autoware_dummy_grid',
        name='autoware_dummy_grid',
        output='screen'
    )

    autoware_planning_node = Node(
        package='autoware_cosim',
        executable='autoware_planning',
        name='autoware_planning',
        output='screen'
    )

    return LaunchDescription([
        # Launch arguments
        control_cav_arg,
        cosim_controlled_vehicle_keys_arg,
        
        # Nodes
        autoware_vehicle_plugin_node,
        autoware_vehicle_report_node,
        autoware_tls_plugin_node,
        autoware_dummy_grid_node,
        autoware_planning_node,
    ]) 