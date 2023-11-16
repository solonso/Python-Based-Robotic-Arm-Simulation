import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
sns.set_theme(style="darkgrid")

def create_time_series(start, end, step):
    """Generate a time series for the animation."""
    return np.arange(start, end + step, step)

def forward_kinematics(joint_angles, joint_lengths):
    """Calculate the positions of all joints in 3D using forward kinematics."""
    x, y, z = 0, 0, 0
    positions = []

    for angles, length in zip(joint_angles, joint_lengths):
        angle_x, angle_y, angle_z = angles
        x += length * np.cos(angle_x) * np.sin(angle_y)
        y += length * np.sin(angle_x) * np.sin(angle_y)
        z += length * np.cos(angle_y)
        positions.append((x, y, z))

    return positions

def figure_eight_trajectory_3d(t, scale=5):
    """Generate a 3D figure-eight trajectory."""
    x = scale * np.sin(2 * np.pi * t)
    y = scale * np.sin(2 * np.pi * t) * np.cos(2 * np.pi * t)
    z = scale * np.cos(2 * np.pi * 2 * t)
    return x, y, z

def simple_inverse_kinematics_3d(x, y, z, joint_lengths):
    """A very simple 3D inverse kinematics for demonstration."""
    l1, l2 = joint_lengths[0], joint_lengths[1]
    angle_x = np.arctan2(y, x)
    angle_y = np.arctan2(np.sqrt(x**2 + y**2), z)
    angle_z = 0  # Keeping this zero for simplicity
    return (angle_x, angle_y, angle_z)

def setup_animation_axes_3d():
    """Set up axes and lines for the 3D animation plot."""
    fig = plt.figure(figsize=(16, 9), dpi=80)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    joint_lines = [ax.plot([], [], [], 'o-', linewidth=2, markersize=4)[0] for _ in range(4)]
    trajectory_line, = ax.plot([], [], [], 'r--', linewidth=1.5)

    return fig, ax, joint_lines, trajectory_line

def animate_3d(frame, joint_angles, joint_lengths, joint_lines, trajectory_line, time_series):
    """Update function for the 3D animation."""
    end_effector_positions = []

    for i in range(frame):
        angles = joint_angles[i]
        positions = forward_kinematics(angles, joint_lengths)
        end_effector_positions.append(positions[-1])

        for j in range(len(joint_lines)):
            xs, ys, zs = zip(*[positions[j-1], positions[j]] if j > 0 else [(0, 0, 0), positions[j]])
            joint_lines[j].set_data(xs, ys)
            joint_lines[j].set_3d_properties(zs)

    if end_effector_positions:
        trajectory_x, trajectory_y, trajectory_z = zip(*end_effector_positions)
        trajectory_line.set_data(trajectory_x, trajectory_y)
        trajectory_line.set_3d_properties(trajectory_z)

    return joint_lines + [trajectory_line]

def main():
    t0, t_end, dt = 0, 30, 0.005
    time_series = create_time_series(t0, t_end, dt)
    joint_lengths = [4, 5, 3, 1.5]

    # Generating joint angles based on 3D figure-eight trajectory
    joint_angles_time_series = []
    for t in time_series:
        x, y, z = figure_eight_trajectory_3d(t)
        angles = simple_inverse_kinematics_3d(x, y, z, joint_lengths[:2])

        # Correctly structure the angles for each joint at this time step
        joint_angles_at_t = [angles, (0, 0, 0), (0, 0, 0), (0, 0, 0)]  # Assuming 4 joints
        joint_angles_time_series.append(joint_angles_at_t)

    fig, ax, joint_lines, trajectory_line = setup_animation_axes_3d()

    ani = animation.FuncAnimation(fig, animate_3d, len(time_series), 
                                  fargs=(joint_angles_time_series, joint_lengths, joint_lines, trajectory_line, time_series), 
                                  interval=25, blit=True)

    plt.show()

if __name__ == "__main__":
    main()