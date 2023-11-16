## Overview

This repository contains Python scripts for simulating the movements of a robotic arm in both 3D and 4D environments. The simulations demonstrate the arm's capability to track complex trajectories and perform intricate movements, showcasing the potential applications in real-life robotics.

### Acknowledgement

Special thanks to Mark Misin for his foundational teachings on Python animations, which greatly influenced this project. His expertise in simulating dynamic systems and movements in programming has been invaluable.

## Features

### Scripts

- `3d-robot-wave.py`: Simulates a robotic arm in a 3D space performing a wave-like motion.
- `4d-robot-unregular.py`: Demonstrates a robotic arm in 4D space executing an irregular trajectory.
- `4d-robot.py`: A 4D robotic arm simulation following a predefined path.

### Function Descriptions

Each script contains several key functions essential for the simulation:

- `create_time_series(start, end, step)`: Generates a time series for controlling the animation frame rate and duration.
- `forward_kinematics(joint_angles, joint_lengths)`: Calculates the position of each joint in the robotic arm, based on the given angles and lengths. This function is crucial for determining how the arm moves through space.
- `figure_eight_trajectory_3d(t, scale)`: Generates a 3D figure-eight trajectory, used as a reference path for the arm's end effector.
- `simple_inverse_kinematics_3d(x, y, z, joint_lengths)`: A simplified approach to inverse kinematics, computing the necessary joint angles to reach a desired point in 3D space.
- `setup_animation_axes_3d()`: Sets up the 3D plotting environment for the simulation.
- `animate_3d(frame, joint_angles, joint_lengths, joint_lines, trajectory_line, time_series)`: The animation loop, updating the positions of the arm's joints and the trajectory line at each frame.

### Kinematics Explained

- **Forward Kinematics**: This is the process of calculating the position of the end effector (tip of the arm) based on given joint angles. It's essential for understanding how each joint movement affects the arm's overall position.
  
- **Inverse Kinematics**: The inverse process, where we determine the required joint angles to reach a specific end effector position. This is more complex but crucial in robotic applications where the arm needs to reach or manipulate specific objects.

## Future Plans and Collaboration

We are actively working on enhancing the robotic arm capabilities. Our ongoing efforts include:

- Refining the simulation accuracy to better mirror real-world dynamics.
- Experimenting with various types of trajectories to expand the arm's versatility.
- Implementing improvements to the physical prototype for advanced functionality and efficiency.

### Join the Community

We invite the community to collaborate on this exciting project. Whether you're skilled in robotics, Python programming, mechanical engineering, or just enthusiastic about robotics, your contribution can make a significant difference.

Let's work together to turn this simulation into a reality!
