# GNSS Decoder Package

This ROS2 package provides a GNSS decoder node that processes IMU, odometry, and GNSS data to publish vehicle pose information.

## Features

- Subscribes to IMU, odometry, and GNSS data
- Converts GPS coordinates to UTM coordinates
- Publishes vehicle pose with covariance
- Integrates with Redis for cosimulation
- Handles coordinate transformations and orientation calculations

## Dependencies

- rclpy
- nav_msgs
- sensor_msgs
- geometry_msgs
- numpy
- scipy
- utm
- terasim_cosim

## Usage

### Building the Package

```bash
# From your workspace root
colcon build --packages-select gnss_decoder
```

### Running the Node

```bash
# Source the workspace
source install/setup.bash

# Run the GNSS decoder node
ros2 run gnss_decoder gnss_decoder
```

## Topics

### Subscribed Topics

- `/ins/imu` (sensor_msgs/Imu) - IMU data
- `/ins/odometry` (nav_msgs/Odometry) - Odometry data  
- `/ins/nav_sat_fix` (sensor_msgs/NavSatFix) - GNSS data

### Published Topics

- `/mcity/cav_pose` (geometry_msgs/PoseWithCovarianceStamped) - Vehicle pose

## Configuration

The node uses UTM offset values that can be modified in the code:
- `UTM_offset = [-277497.10, -4686518.71]`

## License

Apache License 2.0 