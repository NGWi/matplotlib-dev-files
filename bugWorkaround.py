def animation_test():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np
    from matplotlib.colors import Normalize  # Add explicit import for Normalize
    
    file = r'example.dat'
    num_frames = 72
    nx = 8
    ny = 9
    data = np.fromfile(file, np.float32).reshape(num_frames, ny, nx)
    
    # Print data statistics to understand value range
    print(f"Data min: {data.min()}, max: {data.max()}, mean: {data.mean()}")
    print(f"First frame min: {data[0].min()}, max: {data[0].max()}, mean: {data[0].mean()}")

    fig, ax = plt.subplots()
    
    # Calculate normalization limits once for all frames
    vmax = np.percentile(data, 95)  # Use 95th percentile to avoid outliers
    vmin = np.percentile(data, 5)   # Use 5th percentile to avoid outliers
    
    # Create a single normalizer to be used consistently throughout the animation
    norm = Normalize(vmin=vmin, vmax=vmax)
    
    # Use the normalizer in imshow instead of vmin/vmax
    h = ax.imshow(data[0], cmap=plt.get_cmap('CMRmap_r'), origin='lower',
                  interpolation='none', norm=norm, animated=True)
    
    ax.set_xticks(range(nx))
    ax.set_xticklabels(range(1, nx + 1))
    ax.set_yticks(range(ny))
    ax.set_yticklabels(range(1, ny + 1))
    plt.colorbar(h)
    fig.tight_layout()

    def update(frame):
        # Simply update the array data - normalization is handled by our Normalize object
        h.set_array(data[frame])
        return h,

    # Create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(num_frames), 
                                interval=interval, blit=True)
    
    # Save first to ensure consistent state
    # The Normalize object will ensure consistent color scaling in the saved file
    ani.save('example_fixed.gif', writer='pillow', fps=2, dpi=300)
    plt.show()

if __name__ == '__main__':
    animation_test()