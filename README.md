# Digit_sensor
A ROS Package that enables shear force estimation with Facebook's DIGIT Tactile sensors

# Required dependencies:

OpenCV

Digit: https://github.com/facebookresearch/digit-interface

PRMessages: https://github.com/personalrobotics/pr_control_msgs

## You can see a demo here: https://drive.google.com/file/d/1lFl928FAtotZ-w2F6MqtwLAZmR1IUUmk/view

# How to run:

1. Run `catkin build`
2. Run `source devel/setup.bash` from the root directory
3. Run `roscore`
4. Make sure both the f/t sensor and the digit sensor are connected to the computer
5. On separate terminals, run `roslaunch tams_wireless_ft ft.launch`, `roslaunch digit digit.launch` and `roslaunch collector collect.launch` in that order
6. Optionally, run `rosservice call wireless_ft/reset_bias` to tare
7. In the rosbag directory, run `rosbag record -a` to collect data
8. Run `rostopic echo \forque\forqueSensor` to get F/T sensor readings
9. Run `rostopic echo \magnitude` to get magnitudes
