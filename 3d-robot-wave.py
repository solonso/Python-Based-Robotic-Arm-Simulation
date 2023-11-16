import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

def setup_plot():
    """Set up the matplotlib plot for the animation."""
    fig = plt.figure(figsize=(16, 9), dpi=80, facecolor=(0.8, 0.8, 0.8))
    gs = gridspec.GridSpec(3, 3)
    plt.subplots_adjust(left=0.03, bottom=0.035, right=0.99, top=0.97, wspace=0.15, hspace=0.2)
    return fig, gs

def initialize_subplots(fig, gs):
    """Initialize subplots for the animation."""
    ax1 = fig.add_subplot(gs[:, 0:2], facecolor=(0.9, 0.9, 0.9))
    ax1.plot([0, 0], [0, 0.4], 'k', linewidth=20, alpha=0.5)  # base line
    return ax1

def setup_animation_axes(ax1):
    """Set up axes and lines for the main animation plot."""
    ax1.set_xlim(-20, 20)
    ax1.set_ylim(-20, 20)
    ax1.set_xlabel('meters [m]', fontsize=12)
    ax1.set_ylabel('meters [m]', fontsize=12)
    ax1.grid(True)

    joint_lines = [ax1.plot([], [], 'o-', linewidth=2, markersize=4)[0] for _ in range(3)]
    trajectory_line, = ax1.plot([], [], 'b--', linewidth=1.5)  # Distinct trajectory style

    return joint_lines, trajectory_line

def animate_with_sine_wave(frame, joint_angles, joint_lengths, joint_lines, trajectory_line, time_series):
    """Update function for the animation with sine wave trajectory."""
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
    t0, t_end, dt = 0, 30, 0.005  # Extended time range for a clearer sine wave
    time_series = create_time_series(t0, t_end, dt)
    joint_lengths = [5, 3, 5]

    # Sine wave motion for end effector
    sine_wave_amplitude = 3
    sine_wave_frequency = 0.5
    joint_angles = [np.pi/2 * np.sin(2 * np.pi * sine_wave_frequency * time_series) for _ in range(3)]

    fig, gs = setup_plot()
    ax1 = initialize_subplots(fig, gs)
    joint_lines, trajectory_line = setup_animation_axes(ax1)

    ani = animation.FuncAnimation(fig, animate_with_sine_wave, len(time_series), 
                                  fargs=(joint_angles, joint_lengths, joint_lines, trajectory_line, time_series), 
                                  interval=20, blit=True)

    plt.show()

if __name__ == "__main__":
    main()
