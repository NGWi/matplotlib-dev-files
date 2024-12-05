def animation_test():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    num_transixal= 4
    num_axis= 9
    num= num_transixal* num_axis
    N = 2
    ratio_data: np.ndarray  # [72, 9, 8]

    fig, ax = plt.subplots()
    img = ratio_data[0,]
    # plt.imshow(img)
    vmax = 100
    vmin = 0
    h = ax.imshow(img, cmap=plt.get_cmap('CMRmap_r'), origin='lower', interpolation='none', vmin=vmin, vmax=vmax,
                  animated=True)
    ax.set_xticks(range(N * num_transixal))
    ax.set_xticklabels(range(1, N * num_transixal+ 1))
    ax.set_yticks(range(num_axis))
    ax.set_yticklabels(range(1, num_axis+ 1))
    ax.set_title(f'frame: 1')
    fig.tight_layout()


    def update(frame):
        img = ratio_data[frame,]
        # h.set_data(img)
        h.set_array(img)
        ax.set_title(f'frame: {frame}')
        return h,

    # create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(72), interval=interval, blit=True)
    # ani = animation.FuncAnimation(fig, update, frames=frame_iter, interval=interval, blit=False, cache_frame_data=False)
    ani.save('temp.gif', writer='pillow', fps=2, dpi=300)

if __name__ == '__main__':
    animation_test()