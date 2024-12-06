import matplotlib.pyplot as plt
import numpy as np

def create_plot(set_ylim=False, backend='pdf'):
    """Create a bar plot with very small relative differences.
    
    Parameters:
        set_ylim (bool): If True, set y-limits to avoid large transform values
        backend (str): The backend to use ('pdf', 'png', or 'show')
    """
    # Create data with very small relative differences
    base = 4.385
    diff = 0.00001  # 0.001% difference - small enough to trigger PDF rendering issue
    values = [base * (1 + i*diff) for i in range(5)]  # Use multiplier to avoid base value
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Print actual values and their differences
    print(f"\nPlot with{'out' if not set_ylim else ''} ylim ({backend} backend):")
    print("Values and relative differences:")
    for i, v in enumerate(values):
        rel_diff = ((v - values[0]) / values[0]) * 100
        print(f"Val {i+1}: {v:.8f} (diff from Val 1: {rel_diff:.4f}%)")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    if set_ylim:
        # Set y-limits to keep transform matrix values smaller
        min_y = min(values) * 0.99
        max_y = max(values) * 1.01
        ax.set_ylim(min_y, max_y)
    
    # Print transform info
    trans = ax.transData.get_matrix()
    print(f"Transform matrix scale: {trans[1,1]:.2e}")
    
    # Save or show plot
    if backend == 'pdf':
        plt.savefig(f'minimal_{"with" if set_ylim else "without"}_ylim.pdf')
    elif backend == 'png':
        plt.savefig(f'minimal_{"with" if set_ylim else "without"}_ylim.png', dpi=100)
    else:
        plt.show()
    plt.close()

# Test with different backends
for backend in ['pdf', 'png', 'show']:
    create_plot(set_ylim=False, backend=backend)  # Will have invisible bars in PDF
    create_plot(set_ylim=True, backend=backend)   # All bars visible in all formats
