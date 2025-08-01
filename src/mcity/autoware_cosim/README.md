# Autoware Co-simulation Package

This package provides co-simulation capabilities for Autoware with external simulation environments.

## Launch Files

### Main Launch File
The main launch file `autoware_cosim.launch.py` launches all executables in the package:

```bash
ros2 launch autoware_cosim autoware_cosim.launch.py
```

### Individual Component Launch Files
You can also launch individual components:

```bash
# Launch only the vehicle plugin
ros2 launch autoware_cosim autoware_vehicle_plugin.launch.py

# Launch with custom parameters
ros2 launch autoware_cosim autoware_vehicle_plugin.launch.py control_cav:=true
```

## Available Executables

1. **autoware_vehicle_plugin** - Main vehicle interface for co-simulation
2. **autoware_vehicle_report** - Vehicle reporting functionality
3. **autoware_tls_plugin** - Traffic Light System plugin
4. **autoware_dummy_grid** - Dummy grid functionality
5. **autoware_planning** - Planning module

## Launch Arguments

### autoware_vehicle_plugin
- `control_cav` (default: false) - Whether to control CAV from Autoware or Cosim
- `cosim_controlled_vehicle_keys` (default: [TERASIM_ACTOR_INFO]) - List of cosim controlled vehicle keys

## Building

```bash
colcon build --packages-select autoware_cosim
```

## Running

After building, source the workspace and run:

```bash
source install/setup.bash
ros2 launch autoware_cosim autoware_cosim.launch.py
``` 