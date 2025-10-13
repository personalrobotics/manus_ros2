# Manus Teleoperation
This repository utilizes ROS2 and the Manus Gloves to control various grippers. The `manus_ros2` package is from the official site, specifically Manus Core 3.0.1.

Tested on Ubuntu 22.04 with ROS2 Humble/Python 3.10

We currently support the following grippers:
- Alt-Bionic's Surge Hand
- Psyonic's Ability Hand

## Pre-Installation
Due to GitHub's file size limitations, the `lib` folders in ManusSDK are missing. You will need to download `ManusSDK/lib` from the official Manus website. Copy and paste the contents into this repository's `manus_ros2/src/manus_ros2/ManusSDK/lib`.

## Quickstart
1. Build the ROS2 package and source
    ```
    cd manus_ros2
    source /opt/ros/humble/setup.bash
    colcon build
    source install/setup.bash
    ```
2. Connect your Manus Glove(s) to your PC
3. Run the Manus Data Publisher Node
    ```
    ros2 run manus_ros2 manus_data_publisher
    ```
4. Run the corresponding teleoperation script
    ```
    python src/manus_ros2/client_scripts/manus_surge_teleop.py
    ```


## Hand Scaling (with MANUS Gloves and ROS2)
1. Follow the instructions to install [manus_ros2](https://docs.manus-meta.com/3.1.0/Plugins/SDK/ROS2/getting%20started/)
2. Run the Manus data publisher
    ```
    ros2 run manus_ros2 manus_data_publisher
    ```
3. Source the `manus_ros2` package in another terminal and run `ros2 topic echo /manus_glove_0`.

4. Place your hand on a horizontal non-metal surface and close your fingers, but point your thumb outwards.

    <img src="assets/manus_calib_1.jpeg" width=300>

    Note the following joints and their values:
    - ThumbMCPSpread
    - ThumbMCPStretch
    - IndexMCPStretch
    - MiddleMCPStretch
    - RingMCPStretch
    - PinkyMCPStretch

    These values will be the lower bounds for your range.

5. Move your thumb towards your palm.

    <img src="assets/manus_calib_2.jpeg" width=300>

    Note the `ThumbMCPStretch` joint and its value. This is the upper bound of your ThumMCPStretch's range.


6. Position your fingers like a thumbs up

    <img src="assets/manus_calib_3.jpeg" width=300>
    
    Note the following joints and their values:
    - IndexMCPStretch 
    - MiddleMCPStretch 
    - RingMCPStretch 
    - PinkyMCPStretch

    These values will be the upper bounds for your range.

7. While opening your hand and keep your four fingers touching, move the thumb to the base of the pinky finger

    <img src="assets/manus_calib_4.jpeg" width=300>

    Note the `ThumbMCPSpread` joint and its value. This is the upper bound of your ThumbMCPSpread's range

8. Nagivate to your desired teloperation script. In the listener_callback function, modify the formulas to match your individual range.

    The formula to normalize the value is:
    
    <p align="center">
      (<i>ergo_data.value</i> − <i>lower&nbsp;bound</i>) / (<i>upper&nbsp;bound</i> − <i>lower&nbsp;bound</i>) × 100
    </p>

    You may have to perform additional adjustments due to the difference in grippers.
