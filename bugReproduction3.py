def animation_test():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np
    file = r'example.dat'
    num_frames = 72
    nx = 8
    ny = 9
    data = np.fromfile(file, np.float32).reshape(num_frames, ny, nx)
    
    # Print data statistics to understand value range
    print(f"Data min: {data.min()}, max: {data.max()}, mean: {data.mean()}")
    print(f"First frame min: {data[0].min()}, max: {data[0].max()}, mean: {data[0].mean()}")

    fig, ax = plt.subplots()
    img = data[0,]
    
    # Use data range for proper color scaling
    vmax = np.percentile(data, 95)  # Use 95th percentile to avoid outliers
    vmin = np.percentile(data, 5)   # Use 5th percentile to avoid outliers
    
    h = ax.imshow(img, cmap=plt.get_cmap('CMRmap_r'), origin='lower', 
                  interpolation='none', vmin=vmin, vmax=vmax, animated=True)
    ax.set_xticks(range(nx))
    ax.set_xticklabels(range(1, nx + 1))
    ax.set_yticks(range(ny))
    ax.set_yticklabels(range(1, ny + 1))
    plt.colorbar(h)
    fig.tight_layout()

    def update(frame):
        img = data[frame, ]
        h.set_array(img)
        return h,

    # create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(num_frames), interval=interval, blit=True)
    
    # Save first to ensure consistent state
    ani.save('example.gif', writer='pillow', fps=2, dpi=300)
    plt.show()

if __name__ == '__main__':
    animation_test()