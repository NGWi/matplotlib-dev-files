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

def create_plot_mask(shape):
    """Create a mask that excludes axes regions."""
    mask = np.ones(shape[:2], dtype=bool)
    
    # Exclude everything up to and including the left border
    mask[:, :390] = False

    # Exclude bottom axis region
    mask[-150:, :] = False
    
    # Exclude top margin
    mask[:100, :] = False
    
    # Exclude everything up to and including the right border
    mask[:, -495:] = False
    
    # Debug: Save mask visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(mask, cmap='gray')
    plt.title('Plot Region Mask (White = Included, Black = Excluded)')
    plt.savefig('mask_visualization.png')
    plt.close()
    
    return mask

def visualize_difference(direct_rgb, gif_rgb, diff, coords, frame_num):
    """Visualize the difference between frames at the point of maximum difference."""
    y, x = coords
    
    # Create a figure with a 2x3 grid
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot original frame
    axes[0,0].imshow(direct_rgb)
    axes[0,0].set_title('Direct Frame')
    
    # Plot GIF frame
    axes[0,1].imshow(gif_rgb)
    axes[0,1].set_title('GIF Frame')
    
    # Plot difference
    diff_plot = axes[0,2].imshow(np.mean(diff, axis=2), cmap='hot')
    axes[0,2].set_title('Difference Map')
    plt.colorbar(diff_plot, ax=axes[0,2])
    
    # Define zoom region
    zoom_size = 20
    x_start = max(0, x - zoom_size)
    x_end = min(direct_rgb.shape[1], x + zoom_size)
    y_start = max(0, y - zoom_size)
    y_end = min(direct_rgb.shape[0], y + zoom_size)
    
    # Plot zoomed regions with pixel values
    zoom_direct = direct_rgb[y_start:y_end, x_start:x_end]
    zoom_gif = gif_rgb[y_start:y_end, x_start:x_end]
    zoom_diff = np.mean(diff[y_start:y_end, x_start:x_end], axis=2)
    
    axes[1,0].imshow(zoom_direct)
    axes[1,0].set_title(f'Zoomed Direct\nPixel at ({x},{y}): {direct_rgb[y,x]}')
    
    axes[1,1].imshow(zoom_gif)
    axes[1,1].set_title(f'Zoomed GIF\nPixel at ({x},{y}): {gif_rgb[y,x]}')
    
    zoom_diff_plot = axes[1,2].imshow(zoom_diff, cmap='hot')
    axes[1,2].set_title(f'Zoomed Difference\nDiff at ({x},{y}): {diff[y,x]}')
    plt.colorbar(zoom_diff_plot, ax=axes[1,2])
    
    # Mark the maximum difference point
    axes[0,2].plot(x, y, 'r+', markersize=10)  # Correctly place crosshairs on full-frame difference map
    for ax in [axes[1,0], axes[1,1], axes[1,2]]:
        ax.plot(x - x_start, y - y_start, 'r+', markersize=10)
    
    # Print detailed color values
    direct_color = direct_rgb[y, x]
    gif_color = gif_rgb[y, x]
    color_diff = np.abs(direct_color - gif_color)
    
    text = f'Color values at ({x}, {y}):\n'
    text += f'Direct RGB: {direct_color}\n'
    text += f'GIF RGB: {gif_color}\n'
    text += f'Difference: {color_diff}\n'
    text += f'Max channel diff: {np.max(color_diff)}'
    fig.text(0.02, 0.02, text, fontsize=10, family='monospace')
    
    plt.tight_layout()
    plt.savefig(f'frame_{frame_num}_diff.png', dpi=300)
    plt.close()

def compare_animations():
    print("Generating direct matplotlib animation frames...")
    direct_frames = create_animation_and_capture_frames()
    
    print("Capturing frames from saved GIF...")
    gif_frames = capture_gif_frames('example_fixed.gif')
    
    print(f"\nOriginal frame counts:")
    print(f"Direct animation: {len(direct_frames)} frames")
    print(f"GIF: {len(gif_frames)} frames")
    
    direct_frames = direct_frames[2:74]  # Take frames 2 through 73 (72 frames)
    
    print(f"\nAfter selecting animation frames:")
    print(f"Direct animation: {len(direct_frames)} frames")
    print(f"GIF: {len(gif_frames)} frames")
    
    if len(direct_frames) != len(gif_frames):
        print(f"\nERROR: Frame count mismatch!")
        print(f"Direct frames: {len(direct_frames)}, GIF frames: {len(gif_frames)}")
        return
        
    print("\n=== Comparing Frame Colors ===\n")
    
    # Create mask for the plot region
    first_frame = convert_frame_for_comparison(direct_frames[0])
    plot_mask = create_plot_mask(first_frame.shape)
    
    non_identical_frames = []
    max_diff_after_first = 0
    max_diff_details = None
    plot_region_stats = []
    
    for i, (direct_frame, gif_frame) in enumerate(zip(direct_frames, gif_frames)):
        direct_rgb = convert_frame_for_comparison(direct_frame)
        gif_rgb = convert_frame_for_comparison(gif_frame)
        
        if direct_rgb is None or gif_rgb is None:
            print(f"Error: Could not convert frame {i} for comparison")
            continue
        
        # Ensure we're comparing integers
        direct_rgb = direct_rgb.astype(np.uint8)
        gif_rgb = gif_rgb.astype(np.uint8)
        
        # Calculate differences
        diff = np.abs(direct_rgb.astype(int) - gif_rgb.astype(int))
        
        # Calculate statistics for plot region only
        plot_diff = diff[plot_mask]
        plot_stats = {
            'mean': np.mean(plot_diff),
            'max': np.max(plot_diff),
            'std': np.std(plot_diff)
        }
        plot_region_stats.append(plot_stats)
        
        # Full frame statistics for comparison
        max_pixel_diff = np.max(diff)
        mean_diff = np.mean(diff)
        
        if not np.array_equal(direct_rgb, gif_rgb):
            non_identical_frames.append(i)
            
            if i == 0:
                print(f"Frame 0 analysis (palette mode):")
                print(f"Mean color difference: {mean_diff:.4f}")
                print(f"Max pixel difference: {max_pixel_diff:.4f}")
                print(f"Red channel mean difference: {np.mean(diff[..., 0]):.4f}")
                print(f"Green channel mean difference: {np.mean(diff[..., 1]):.4f}")
                print(f"Blue channel mean difference: {np.mean(diff[..., 2]):.4f}\n")
            else:
                # Find location of maximum difference within plot region
                masked_mean_diff = np.mean(diff, axis=2).copy()
                masked_mean_diff[~plot_mask] = -1
                
                # Find all points with actual differences
                diff_points = np.argwhere(masked_mean_diff > 0)
                if len(diff_points) > 0:
                    # Find the point with maximum difference among valid points
                    max_diff_point_idx = np.argmax([masked_mean_diff[y,x] for y,x in diff_points])
                    y, x = diff_points[max_diff_point_idx]
                    
                    current_max_diff = np.max(diff[y,x])
                    if current_max_diff > max_diff_after_first:
                        max_diff_after_first = current_max_diff
                        max_diff_frame = i
                        max_diff_details = {
                            'coords': (y, x),
                            'mean': mean_diff,
                            'max': current_max_diff,
                            'red': np.mean(diff[..., 0]),
                            'green': np.mean(diff[..., 1]),
                            'blue': np.mean(diff[..., 2]),
                            'direct_rgb': direct_rgb,
                            'gif_rgb': gif_rgb,
                            'diff': diff
                        }
                        
                        # Debug output
                        print(f"\nDebug: Frame {i} maximum difference found:")
                        print(f"Location: ({x}, {y})")
                        print(f"Direct RGB: {direct_rgb[y, x]}")
                        print(f"GIF RGB: {gif_rgb[y, x]}")
                        print(f"Difference: {diff[y, x]}")
                        print(f"Is in mask?: {plot_mask[y, x]}")
    
    # Convert stats to numpy array for easier analysis
    plot_region_stats = np.array([(s['mean'], s['max'], s['std']) for s in plot_region_stats])
    
    print("\n=== Plot Region Analysis (excluding axes) ===")
    print(f"Mean difference: {np.mean(plot_region_stats[1:, 0]):.4f}")  # Exclude first frame
    print(f"Max difference: {np.max(plot_region_stats[1:, 1]):.4f}")
    print(f"Standard deviation: {np.mean(plot_region_stats[1:, 2]):.4f}")
    
    print("\n=== Exact Frame Comparison Results ===")
    if len(non_identical_frames) == 0:
        print("All frames are exactly identical!")
    else:
        print(f"Found {len(non_identical_frames)} non-identical frames")
        print(f"Frame numbers: {non_identical_frames}")
        
        if max_diff_details is not None:
            y, x = max_diff_details['coords']
            print(f"\nLargest difference in non-palette frames (Frame {max_diff_frame}):")
            print(f"Location: (x={x}, y={y})")
            print(f"Mean color difference: {max_diff_details['mean']:.4f}")
            print(f"Max pixel difference: {max_diff_details['max']:.4f}")
            print(f"Red channel mean difference: {max_diff_details['red']:.4f}")
            print(f"Green channel mean difference: {max_diff_details['green']:.4f}")
            print(f"Blue channel mean difference: {max_diff_details['blue']:.4f}")
            
            visualize_difference(
                max_diff_details['direct_rgb'],
                max_diff_details['gif_rgb'],
                max_diff_details['diff'],
                max_diff_details['coords'],
                max_diff_frame
            )
            print(f"\nVisualization saved as frame_{max_diff_frame}_diff.png")

if __name__ == '__main__':
    compare_animations()
