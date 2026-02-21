# Manus Teleoperation
This repository utilizes ROS2 and the Manus Gloves to control various grippers. The `manus_ros2` package is from the official site, specifically Manus Core 3.1,0.

Tested on Ubuntu 22.04 with ROS2 Humble/Python 3.10

We currently support the following grippers:
- [Alt-Bionic's Surge Hand](https://github.com/personalrobotics/surge-hand-api)
- [Psyonic's Ability Hand](https://github.com/psyonicinc/ability-hand-api)

## Pre-Installation
Due to GitHub's file size limitations, the `lib` folders in ManusSDK are missing. You will need to download the SDK to obtain `ManusSDK` from the [official Manus website](https://docs.manus-meta.com/3.1.0/Resources/). Copy and replace the contents of this repository's `manus_ros2/src/manus_ros2/ManusSDK`.

## Quickstart
1. Clone this repository into your workspace
```bash
git clone https://github.com/personalrobotics/manus_ros2.git
```
2. If you haven't already, clone `ManusSDK/lib` into your workspace
```bash
sudo cp -r /path/to/MANUS_Core_3.1.0_SDK/ManusSDK_v3.1.0/ROS2/ManusSDK /path/to/your_workspace/src/manus_ros2/src/manus_ros2/
```
2. Install dependencies
```bash
sudo apt-get update && sudo apt-get install -y build-essential git libtool libzmq3-dev libusb-1.0-0-dev zlib1g-dev libudev-dev gdb libncurses5-dev && sudo apt-get clean
```
```bash
sudo git clone -b v1.28.1 https://github.com/grpc/grpc /var/local/git/grpc && cd /var/local/git/grpc && sudo git submodule update --init --recursive
```
```bash
cd /var/local/git/grpc/third_party/protobuf && sudo ./autogen.sh && sudo ./configure --enable-shared && sudo make -j$(nproc) && sudo make -j$(nproc) check && sudo make install && sudo make clean && sudo ldconfig
```
```bash
cd /var/local/git/grpc && sudo make -j$(nproc) && sudo make install && sudo make clean && sudo ldconfig
```
```bash
pip install catkin_pkg 'empy<4' numpy lark mujoco
```
(optional depending on which hand(s) you're using)
```bash
cd your-workspace/src

# Psyonic Ability Hand API
git clone git@github.com:psyonicinc/ability-hand-api.git
cd ability-hand-api/python
pip install -e .
export PYTHONPATH=$PYTHONPATH:path/to/ability-hand-api/python

# Surge Hand API
git clone https://github.com/personalrobotics/surge-hand-api.git
export PYTHONPATH=$PYTHONPATH:path/to/surge-hand-api/python
```

3. To allow connections to MANUS hardware you need to place the following file in the etc/udev/rules.d/ directory. This will allow the devices to be recognized and accessed by the system. After doing this, a full reboot is recommended to apply the changes. The naming of the file is relevant we recommend naming it `70-manus-hid.rules`.
```bash
# HIDAPI/libusb
SUBSYSTEMS=="usb", ATTRS{idVendor}=="3325", MODE:="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="83fd", MODE:="0666"

# HIDAPI/hidraw
KERNEL=="hidraw*", ATTRS{idVendor}=="3325", MODE:="0666"
```
4. Build the ROS2 package and source
```bash
cd src/manus_ros2
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```
2. Connect your Manus Glove(s) to your PC
3. Run the Manus Data Publisher Node
```bash
ros2 run manus_ros2 manus_data_publisher
```
4. Run the corresponding teleoperation script
```bash
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
