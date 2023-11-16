import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
sns.set_theme(style="darkgrid")

def create_time_series(start, end, step):
    """Generate a time series for the animation."""
    return np.arange(start, end + step, step)

def forward_kinematics(joint_angles, joint_lengths):
    """Calculate the positions of all joints using forward kinematics."""
    x, y = 0, 0
    cumulative_angle = 0
    positions = []

    for angle, length in zip(joint_angles, joint_lengths):
        cumulative_angle += angle
        x += length * np.cos(cumulative_angle)
        y += length * np.sin(cumulative_angle)
        positions.append((x, y))

    return positions

def setup_animation_axes():
    """Set up axes and lines for the animation plot."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=80, facecolor=(0.8, 0.8, 0.8))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xlabel('meters [m]', fontsize=12)
    ax.set_ylabel('meters [m]', fontsize=12)
    ax.grid(True)

    joint_lines = [ax.plot([], [], 'o-', linewidth=2, markersize=4)[0] for _ in range(4)]
    trajectory_line, = ax.plot([], [], 'r--', linewidth=1.5)  # Distinct trajectory style

    return fig, joint_lines, trajectory_line

def animate(frame, joint_angles, joint_lengths, joint_lines, trajectory_line, time_series):
    """Update function for the animation with a complex trajectory."""
    end_effector_positions = []

    for i in range(frame):
        angles = [joint_angle[i] for joint_angle in joint_angles]
        positions = forward_kinematics(angles, joint_lengths)
        end_effector_positions.append(positions[-1])  # Append only the end effector position

        for j in range(len(joint_lines)):
            if j == 0:
                joint_lines[j].set_data([0, positions[j][0]], [0, positions[j][1]])
            else:
                joint_lines[j].set_data([positions[j-1][0], positions[j][0]], 
                                        [positions[j-1][1], positions[j][1]])

    if end_effector_positions:
        trajectory_x, trajectory_y = zip(*end_effector_positions)
        trajectory_line.set_data(trajectory_x, trajectory_y)

    return joint_lines + [trajectory_line]

def main():
    t0, t_end, dt = 0, 30, 0.005
    time_series = create_time_series(t0, t_end, dt)
    joint_lengths = [4, 3, 2, 1.5]
    joint_angles = [
        np.sin(2 * np.pi * 0.5 * time_series) + np.sin(2 * np.pi * 0.2 * time_series),
        np.cos(2 * np.pi * 0.5 * time_series),
        np.sin(2 * np.pi * 0.5 * time_series) - np.cos(2 * np.pi * 0.5 * time_series),
        np.cos(2 * np.pi * 0.5 * time_series) + np.sin(2 * np.pi * 0.1 * time_series)
    ]

    fig, joint_lines, trajectory_line = setup_animation_axes()

    ani = animation.FuncAnimation(fig, animate, len(time_series), 
                                  fargs=(joint_angles, joint_lengths, joint_lines, trajectory_line, time_series), 
                                  interval=20, blit=True)

    plt.show()

if __name__ == "__main__":
    main()

