# Autoware

This is the Mcity-adapted version of Autoware Universe, based on the October 2023 release and extensively modified. If you are looking for the most up-to-date Autoware Universe, please check out the official [**Documentation**](https://autowarefoundation.github.io/autoware-documentation/main/).


## Prerequisites

- __Hardware__: A CPU based on Intel x86 architecture with at least 16 cores, at least 16 GB of system memory, and a dedicated GPU with at least 8 GB of VRAM.

- __System__: Ubuntu 22.04 (native system installation rather than a virtual machine or Windows Subsystem for Linux)

- __Software__: Follow the official instructions to install [**ROS Humble Desktop**](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

## Installation

### Install dependencies

```bash
sudo apt-get install libhiredis-dev libgeographic-dev ccache python3-rosdep2 python3-colcon-common-extensions ros-humble-rmw-cyclonedds-cpp
```

### Clone the repository

```bash
git clone https://github.com/michigan-traffic-lab/autoware.git
```

### Navigate to the Autoware directory

```bash
cd autoware
```

### Source the ROS distribution

```bash
source /opt/ros/humble/setup.bash
```

### Initialize rosdep

```bash
rosdep init
rosdep update
```

### Open a new terminal and install ROS 2 package dependencies

```bash
rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
```

### Build the workspace

```bash
# This may take 2–4 hours depending on hardware. You can limit the number of parallel build jobs based on your available CPU cores and memory.
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 8
```

### Post Installation Instructions

We recommend running the following to automatically configure your environment each time a new terminal is opened. This ensures that ROS Humble, Autoware, and Cyclone DDS are properly sourced and available by default.

```bash
# Source ROS Humble setup
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Source Autoware workspace setup
echo "source ~/autoware/install/setup.bash" >> ~/.bashrc

# Set Cyclone DDS as the default RMW implementation
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
```


## Run Autoware

### Planning Simulator

```bash
ros2 launch autoware_launch planning_simulator.launch.xml map_path:=$HOME/autoware/map vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit lanelet2_map_file:=lanelet2_mcity_v43.osm
```

To run a quick startup demonstration, first initialize the ego vehicle's state by selecting **"2D Pose Estimate"** at the top of the RViz panel, then set the destination using **"2D Goal Pose"**. Finally, click **"Auto"** on the Operation Mode panel to start the vehicle. If Autoware consistently fails to plan a trajectory, See [**Troubleshooting**](#Troubleshooting) for a potential fix.

![tutorial](figure/startup_tutorial.gif)

Alternatively, to automate the pose initialization, goal selection, and engagement process when launching the Autoware stack, run the provided Mcity route script. The source code is available at `src/mcity/mcity_route` and can be customized as needed.

![route](figure/route.gif)

### Real-Car Stack

```bash
ros2 launch autoware_launch autoware.launch.xml map_path:=$HOME/autoware/map vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit lanelet2_map_file:=lanelet2_mcity_v43.osm
```

We provide a co-simulation interface that integrates the Autoware real-car stack with the high-fidelity CARLA simulator and the traffic generation platform TeraSim. For detailed setup and usage instructions, refer to the [**Terasim**](https://github.com/michigan-traffic-lab/TeraSim) repository.

![cosim](figure/carla.gif)
![cosim](figure/autoware.gif)

### Autoware ROS Bag Replay
```bash
ros2 launch autoware_launch logging_simulator.launch.xml map_path:=$HOME/autoware/map vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit lanelet2_map_file:=lanelet2_mcity_v43.osm
```

## Troubleshooting
If Autoware fails to plan a trajectory after setting a **"2D Goal Pose"**, open a new terminal, run the following command, then relaunch Autoware and try again:

```bash
ros2 run autoware_cosim autoware_dummy_grid
```