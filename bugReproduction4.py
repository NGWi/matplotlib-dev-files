def animation_test():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np

    file = r'example.dat'
    num_frames = 72
    nx = 8
    ny = 9
    data = np.fromfile(file, np.float32).reshape(num_frames, ny, nx)

    fig, ax = plt.subplots()
    img = data[0,]
    # plt.imshow(img)
    vmax = 100
    vmin = 0
    h = ax.imshow(img, cmap=plt.get_cmap('CMRmap_r'), origin='lower', interpolation='none', vmin=vmin, vmax=vmax, animated=True)
    ax.set_xticks(range(nx))
    ax.set_xticklabels(range(1, nx + 1))
    ax.set_yticks(range(ny))
    ax.set_yticklabels(range(1, ny + 1))
    fig.tight_layout()

    def update(frame):
        img = data[frame, ]
        h.set_array(img)
        return h,

    # create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(num_frames), interval=interval, blit=True)
    # ani = animation.FuncAnimation(fig, update, frames=frame_iter, interval=interval, blit=False, cache_frame_data=False)
    plt.show()
    ani.save('example.gif', writer='pillow', fps=2, dpi=300)

    pass

if __name__ == '__main__':
    animation_test()