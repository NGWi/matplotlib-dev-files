import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image
import io
from pathlib import Path
import numpy.testing as npt

def create_animation_and_capture_frames():
    # Load the same data
    file = r'example.dat'
    nx = 8
    ny = 9
    num_frames = 72
    data = np.fromfile(file, np.float32).reshape(num_frames, ny, nx)
    
    # Create figure and plot
    fig, ax = plt.subplots()
    
    vmax = 100
    vmin = 0
    
    h = ax.imshow(data[0], cmap=plt.get_cmap('CMRmap_r'), origin='lower', 
                  interpolation='none', vmin=vmin, vmax=vmax, animated=True)
    
    ax.set_xticks(range(nx))
    ax.set_xticklabels(range(1, nx + 1))
    ax.set_yticks(range(ny))
    ax.set_yticklabels(range(1, ny + 1))
    
    plt.colorbar(h)
    fig.tight_layout()

    # List to store direct frames
    direct_frames = []

    def capture_frame(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        img = Image.open(buf)
        # Print transparency info for first and last few frames
        if len(direct_frames) < 2 or len(direct_frames) > num_frames - 2:
            print(f"\nFrame {len(direct_frames)} transparency info:")
            print(f"Mode: {img.mode}")
            if img.mode in ('RGBA', 'LA'):
                alpha_extrema = img.getchannel('A').getextrema()
                print(f"Alpha channel extrema: {alpha_extrema}")
        return np.array(img)

    def update(frame):
        img = data[frame,]
        h.set_array(img)
        direct_frames.append(capture_frame(fig))
        return h,

    # Create animation
    interval = 100
    ani = animation.FuncAnimation(fig, update, frames=range(num_frames),
                                interval=interval, blit=True)
    
    # Save animation
    ani.save('example_fixed.gif', writer='pillow', fps=2, dpi=300)
    plt.close()  # Close the figure to free memory
    
    return direct_frames

def capture_gif_frames(gif_path):
    gif_frames = []
    gif = Image.open(gif_path)
    
    frame_num = 0
    try:
        while True:
            # Print info about first and last few frames
            if frame_num < 2 or frame_num > 69:
                print(f"\nGIF Frame {frame_num} info:")
                print(f"Mode: {gif.mode}")
                if hasattr(gif, 'info'):
                    print(f"Frame info: {gif.info}")
            
            gif_frames.append(np.array(gif))
            frame_num += 1
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    
    return gif_frames

def convert_frame_for_comparison(frame):
    """Convert frame to RGB for comparison, handling different formats."""
    if isinstance(frame, np.ndarray):
        if frame.ndim == 2:  # Palette mode
            # Convert to RGB by repeating the channel
            return np.stack([frame] * 3, axis=-1)
        elif frame.shape[-1] == 4:  # RGBA
            return frame[..., :3]  # Take only RGB channels
        elif frame.shape[-1] == 3:  # RGB
            return frame
    return None

def compare_animations():
    print("Generating direct matplotlib animation frames...")
    direct_frames = create_animation_and_capture_frames()
    
    print("Capturing frames from saved GIF...")
    gif_frames = capture_gif_frames('example_fixed.gif')
    
    print(f"\nOriginal frame counts:")
    print(f"Direct animation: {len(direct_frames)} frames")
    print(f"GIF: {len(gif_frames)} frames")
    
    # The direct animation has 74 frames total:
    # - Frames 0,1 are setup frames
    # - Frames 72,73 are cleanup frames
    # The actual animation frames are 2 through 73 (72 frames)
    direct_frames = direct_frames[2:74]  # Take frames 2 through 73 (72 frames)
    
    print(f"\nAfter selecting animation frames:")
    print(f"Direct animation: {len(direct_frames)} frames")
    print(f"GIF: {len(gif_frames)} frames")
    
    if len(direct_frames) != len(gif_frames):
        print(f"\nERROR: Frame count mismatch!")
        print(f"Direct frames: {len(direct_frames)}, GIF frames: {len(gif_frames)}")
        return
        
    print("\n=== Comparing Frame Colors ===\n")
    
    frame_differences = []
    max_diff = 0
    max_frame = 0
    
    for i, (direct_frame, gif_frame) in enumerate(zip(direct_frames, gif_frames)):
        # Convert frames to RGB numpy arrays for comparison
        direct_rgb = convert_frame_for_comparison(direct_frame)
        gif_rgb = convert_frame_for_comparison(gif_frame)
        
        if direct_rgb is None or gif_rgb is None:
            print(f"Error: Could not convert frame {i} for comparison")
            continue
            
        # Calculate color differences
        diff = np.abs(direct_rgb.astype(float) - gif_rgb.astype(float))
        mean_diff = np.mean(diff)
        frame_differences.append(mean_diff)
        
        if i == 0:
            print(f"Frame 0 analysis:")
            print(f"Mean color difference: {mean_diff:.4f}")
            print(f"Max pixel difference: {np.max(diff):.4f}")
            print(f"Red channel mean difference: {np.mean(diff[..., 0]):.4f}")
            print(f"Green channel mean difference: {np.mean(diff[..., 1]):.4f}")
            print(f"Blue channel mean difference: {np.mean(diff[..., 2]):.4f}\n")
        
        frame_max = np.max(diff)
        if frame_max > max_diff:
            max_diff = frame_max
            max_frame = i
    
    frame_differences = np.array(frame_differences)
    
    print("=== Overall Analysis ===")
    print(f"Maximum pixel difference across all frames: {max_diff:.4f} (Frame {max_frame})")
    print(f"Average frame difference: {np.mean(frame_differences):.4f}")
    print(f"Standard deviation of frame differences: {np.std(frame_differences):.4f}\n")
    
    # Calculate statistics excluding first frame
    frame_differences_no_first = frame_differences[1:]
    print("=== Analysis Excluding First Frame ===")
    print(f"Maximum pixel difference: {np.max(frame_differences_no_first):.4f}")
    print(f"Average frame difference: {np.mean(frame_differences_no_first):.4f}")
    print(f"Standard deviation of frame differences: {np.std(frame_differences_no_first):.4f}\n")
    
    if np.max(frame_differences) > 0:
        print("Note: Some frames show color differences.")
        print("This is expected due to GIF color palette optimization.")

if __name__ == '__main__':
    compare_animations()
