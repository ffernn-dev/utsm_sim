## 1. Introduction
Automatic Emergency Braking (AEB) is an active safety system in autonomous and driver assistance systems that proactively aims to avoid collisions or reduce as much kinetic energy as possible. It monitors a range of sensors, in this case LiDAR, odometry and steering to predict Time to Collision (TTC) and apply the brakes if required in order to avoid a collision.
The goal of this task is to firstly build an AEB system in a ROS2 environment that calculates a collision risk based on sensor data, and commands the vehicle to brake when required. The system must then be integrated into the existing `utsm_sim` vehicle simulation and evaluated for effectiveness.
TODO: The overall approach taken to complete the task

## 2. Background Research
### 2.1 Automatic Emergency Braking
AEB systems are designed to address the inadequacy of human reaction time when it comes to responding to high-speed danger on the road or, in autonomous systems, act as a failsafe in the event that the system's  pathfinding is unable to avoid a collision. They achieve this by calculating the Time to Collision based on sensor data, and applying the vehicle's brakes if it falls below a threshold (often set using by the estimated braking distance). In cars, the sensor suite for AEB is often a mix of radar, LiDAR, cameras, and velocity data. This sensor data is combined to gain an understanding of the car's distance to its surroundings and the TTC.
### 2.2 Time to Collision
In the case of a moving vehicle and a static object, Time to Collision refers to the minimal time until the vehicle and object collide. The full Time to Collision calculation takes into account the velocity of both entities, the distance between them, as well as their accelerations. The simplified Instantaneous Time to Collision (iTTC) ignores acceleration, which makes it less tolerant to sensor noise and acceleration controls from other safety systems, however it is sufficient for this task. The mathematical formulation for iTTC is as follows:

$$
iTTC = \frac{d}{v}
$$
Where $d$ is the distance between the vehicle and the obstacle and $v$ is the component of the vehicle's velocity toward the obstacle. We must also consider the case where $v \leq 0$, in which case collision is not impending, and $iTTC$ should be taken as $\infty$.
iTTC aids with collision prediction by telling the system how much reaction time is left before a collision occurs. As the iTTC gets closer to zero, the chances of avoiding the collision get much lower no matter the speed.
### 2.3 Relevant ROS2 Concepts
ROS2 is a middleware for robotics and other mechatronics systems, such as autonomous vehicles. It includes drivers, tools, algorithms and a data communications layer to simplify the development of robotic systems. The basic architecture consists of Nodes and Topics.
- Nodes are modular programs that generally only do one thing, such as reading a single sensor's data or running an algorithm.
- A node can have 1 or more Publishers or Subscribers. A Publisher transmits data to a specific "channel" called a topic. A Subscriber "listens" to a topic and processes new data when it arrives from the publisher. This architecture allows for a complete separation of concerns, where the specific implementations of each node can be changed at will, as long as the data they publish/subscribe to is the same.
- A Topic is, at its core, a string that names the channel (e.g. `/odometry`, `/laserscan`). Topics act as the meeting point between Publishers and Subscribers as described above. Topics can be One-to-Many, i.e. a sensor, or Many-to-One, i.e. 4 wheel speed sensors publishing to `/odometry`.
The message types used in the AEB system are:

| Message Type | Purpose |
| ------------ | ------- |
|              |         |
# 3. System design
### 3.1 System Overview


## Notepad
- RViz window was too big for the VNC screen on my laptop. I worked out that the provided Window Manager was Fluxbox, and did some googling to find that I can use alt+rightmouse drag (ended up being cmd + rightmouse on macOS) to resize a window without being able to grab the bottom corners (which I couldn't because the window was too big for the screen 🤦🏻). A better solution may be trying to get noVNC to update 
- The simulation is more usable if you set the fixed frame to the car's `ego_racecar/laser` so that the car stays centred while you drive it.
- The file structure of the git repo is pretty hard to find your way around for a newcomer. It took me a while to find the best places to build my nodes.
- I'm getting the itch to build a new simulation frontend using web technologies so that we don't need to run a whole X11 window manager through a browser on non-ubuntu platforms. That would also allow us to include teleop controls, and even the use of game controllers using the Gamepad API for easier control (helpful for when we're developing SLAM algorithms and such before we have a proper pathfinding system)
- In `rosgym/rosgym/gym_bridge.py:L49` we define the parameter `ego_drive_topic` as `"opp_drive_topic"`. Everything seems to work as is so I don't want to change that but something to have a look at?
- I had some confusion between /ego_racecar/laser and /scan. 
- My IDE's autoformatting applied to some files I worked on so maybe a shared .prettierrc file is a good idea?
