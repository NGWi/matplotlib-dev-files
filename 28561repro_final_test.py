import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test configurations
configs = [
    {'diff': 0.00010, 'width': 8, 'height': 4, 'ylim': False},  # Base case
    {'diff': 0.00010, 'width': 8, 'height': 4, 'ylim': True},   # With ylim
    {'diff': 0.00010, 'width': 4, 'height': 8, 'ylim': False},  # Tall
    {'diff': 0.00009, 'width': 8, 'height': 4, 'ylim': False},  # Different diff
    {'diff': 0.00009, 'width': 8, 'height': 4, 'ylim': True},   # Different diff with ylim
    {'diff': 0.00009, 'width': 4, 'height': 8, 'ylim': False},  # Different diff tall
]

def analyze_transform(ax, values, labels):
    """Detailed transform analysis"""
    # Get data transform components
    trans = ax.transData.get_matrix()
    
    # Get transformed positions for each bar
    positions = []
    for value in values:
        # Get both bottom and top of bar
        bottom = ax.transData.transform([[0, value]])[0]
        top = ax.transData.transform([[0, value * 1.001]])[0]  # Slightly above
        positions.append((bottom[1], top[1]))
    
    print("\nTransform matrix:")
    print(trans)
    print("\nBar positions (bottom, top):")
    for label, value, (bottom, top) in zip(labels, values, positions):
        print(f"{label}: value={value:.8f}, y_pos=({bottom:.2e}, {top:.2e})")
        print(f"    height in points: {top-bottom:.2e}")

# Create and save plots for each configuration
for i, config in enumerate(configs):
    # Create figure
    fig, ax = plt.subplots(figsize=(config['width'], config['height']))
    
    # Create data
    base = 4.385
    offset = 0.1
    diff = config['diff']
    values = [base + offset + i*base*diff for i in range(1, 6)]  # Start from 1 instead of 0
    labels = [f"Val {i}" for i in range(1, 6)]
    
    # Calculate relative range
    rel_range = (max(values) - min(values)) / np.mean(values) * 100
    
    # Create bar plot
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    # Always set a minimum y-limit slightly below the minimum value
    min_y = min(values) * 0.99  # 1% below minimum
    max_y = max(values) * 1.01  # 1% above maximum
    ax.set_ylim(min_y, max_y)
    
    # Set title and analyze
    title = (f"Test {i+1}: {diff*100:.4f}% diff, {config['width']}x{config['height']}, "
            f"{'ylim' if config['ylim'] else 'no ylim'}")
    ax.set_title(title)
    print(f"\n{title}")
    analyze_transform(ax, values, labels)
    
    plt.tight_layout()
    plt.savefig(f'final_test_{i+1}.pdf')
    plt.close()

print("\nFiles saved as final_test_*.pdf")
