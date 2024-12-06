import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

def create_plot(set_ylim=False, backend='pdf'):
    """Create a bar plot with very small relative differences.
    
    Parameters:
        set_ylim (bool): If True, set y-limits to avoid large transform values
        backend (str): The backend to use ('pdf', 'png', or 'show')
    """
    # Create data with very small relative differences
    base = 4.385
    diff = 0.00001  # 0.001% difference
    values = [base * (1 + i*diff) for i in range(5)]
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Print actual values and their differences
    print(f"\nPlot with{'out' if not set_ylim else ''} ylim ({backend} backend):")
    print("Values and relative differences:")
    for i, v in enumerate(values):
        rel_diff = ((v - values[0]) / values[0]) * 100
        print(f"Val {i+1}: {v:.8f} (diff from Val 1: {rel_diff:.4f}%)")
    
    # Normalize values relative to their mean
    mean_val = sum(values) / len(values)
    normalized_values = [(v - mean_val) / mean_val * 100 for v in values]  # Convert to percentage difference from mean
    
    # Create plot with optimized size for PDF
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, normalized_values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, zorder=1)
    
    # Add value labels above or below bars depending on their value
    for bar in bars:
        height = bar.get_height()
        label_y = height + 0.0001 if height >= 0 else height - 0.0002
        va = 'bottom' if height >= 0 else 'top'
        ax.text(bar.get_x() + bar.get_width()/2, label_y,
                f'{height:.4f}%', ha='center', va=va)
    
    if set_ylim:
        max_diff = max(normalized_values)
        min_diff = min(normalized_values)
        # Set limits to ensure all bars and labels are visible
        padding = max(abs(max_diff), abs(min_diff)) * 0.2
        ax.set_ylim(min_diff - padding, max_diff + padding)
    
    ax.set_ylabel('Relative Difference from Mean (%)')
    ax.set_title('Values Shown as Percentage Difference from Mean')
    
    # Print transform info
    trans = ax.transData.get_matrix()
    print(f"Transform matrix scale: {trans[1,1]:.2e}")
    
    # Save or show plot with optimized PDF settings
    if backend == 'pdf':
        with PdfPages(f'minimal_{("with" if set_ylim else "without")}_ylim.pdf') as pdf:
            plt.savefig(pdf, format='pdf', dpi=300)
    elif backend == 'png':
        plt.savefig(f'minimal_{("with" if set_ylim else "without")}_ylim.png', dpi=300)
    else:
        plt.show()
    plt.close()

# Test with different backends
for backend in ['pdf', 'png', 'show']:
    create_plot(set_ylim=False, backend=backend)  # Will have invisible bars in PDF
    create_plot(set_ylim=True, backend=backend)   # All bars visible in all formats
