import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animation_test():
    # Define the number of blocks, axes, and translations
    num_transixal = 4
    num_axis = 9
    num = num_transixal * num_axis
    N = 2

    # Create a sample data array
    ratio_data = np.zeros((72, num_axis, N * num_transixal))

    # Set the values for the blocks in the data array
    for i in range(num_transixal):
        for j in range(num_axis):
            block_index = i * num_axis + j
            ratio_data[block_index, j, i*2: i*2+2] = 100

    # Create the plot
    fig, ax = plt.subplots()
    img = ratio_data[0]
    vmax = 100
    vmin = 0
    h = ax.imshow(img, cmap=plt.get_cmap('CMRmap_r'), origin='lower', interpolation='none', vmin=vmin, vmax=vmax, animated=True)

    # Set axis ticks and labels
    ax.set_xticks(np.arange(0, N * num_transixal, 2) + 0.5)
    ax.set_xticklabels(range(1, N * num_transixal+ 1, 2))
    ax.set_yticks(np.arange(num_axis))
    ax.set_yticklabels(range(1, num_axis+ 1))

    # Set initial title
    ax.set_title(f'frame: 1')
    fig.tight_layout()

    def update(frame):
        img = ratio_data[frame]
        h.set_array(img)
        ax.set_title(f'frame: {frame + 1}')  # Adjust frame title to be 1-indexed
        return h,

    # Create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(72), interval=interval, blit=True)
    ani.save('temp.gif', writer='pillow', fps=2, dpi=300)

if __name__ == '__main__':
    animation_test()