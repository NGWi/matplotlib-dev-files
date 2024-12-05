import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image

def create_animation():
    # Load the same data
    file = r'example.dat'
    nx = 8
    ny = 9
    num_frames = 72
    data = np.fromfile(file, np.float32).reshape(num_frames, ny, nx)
    
    # Create figure and plot
    fig, ax = plt.subplots()
    
    # Use exactly the same parameters as bugReproduction4.py
    vmax = 100
    vmin = 0
    
    # Create plot exactly like bugReproduction4.py
    h = ax.imshow(data[0], cmap=plt.get_cmap('CMRmap_r'), origin='lower', 
                  interpolation='none', vmin=vmin, vmax=vmax, animated=True)
    
    # Set the same axis labels
    ax.set_xticks(range(nx))
    ax.set_xticklabels(range(1, nx + 1))
    ax.set_yticks(range(ny))
    ax.set_yticklabels(range(1, ny + 1))
    
    plt.colorbar(h)
    fig.tight_layout()

    def update(frame):
        img = data[frame,]
        h.set_array(img)
        return h,

    # Create animation with same parameters
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(num_frames),
                                interval=interval, blit=True)
    
    # Save first, then show - exactly like bugReproduction4.py
    ani.save('example_fixed.gif', writer='pillow', fps=2, dpi=300)
    plt.show()

def display_saved_gif():
    # Load the gif using PIL
    gif = Image.open('example_fixed.gif')
    
    # Create figure and axis
    fig, ax = plt.subplots()
    
    def update(frame):
        # Seek to frame
        gif.seek(frame)
        # Convert PIL image to array and display
        ax.clear()
        ax.imshow(gif)
        return ax,
    
    # Get number of frames
    n_frames = 0
    try:
        while True:
            gif.seek(n_frames)
            n_frames += 1
    except EOFError:
        gif.seek(0)
    
    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=range(n_frames),
                                interval=500, blit=True)
    plt.show()

if __name__ == '__main__':
    create_animation()
    print("\nNow displaying the saved gif:")
    display_saved_gif()
