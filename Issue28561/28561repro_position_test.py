import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test 0.0009% with different figure heights
heights = [4, 6, 8]  # Different figure heights to test
diff = 0.000009  # The case that showed no bars

def analyze_transform(ax, title, values, labels):
    """Analyze transformation matrices in detail"""
    print(f"\n{title}")
    print("Bar positions:")
    for label, value in zip(labels, values):
        display_pos = ax.transData.transform([[0, value]])[0]
        print(f"{label}: value={value:.8f}, y_transform={display_pos[1]:.2e}")

# Create plots with different heights
for height in heights:
    fig, ax = plt.subplots(figsize=(8, height))
    
    # Create data
    base = 4.385
    values = [base + i*base*diff for i in range(5)]
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Calculate relative range
    rel_range = (max(values) - min(values)) / np.mean(values) * 100
    
    # Create bar plot
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    # Analyze transforms
    title = f'Height {height}: Diff {diff*100:.4f}% (range: {rel_range:.4f}%)'
    ax.set_title(title)
    analyze_transform(ax, title, values, labels)
    
    plt.tight_layout()
    plt.savefig(f'position_test_h{height}.pdf')
    plt.close()

print("\nFiles saved as position_test_h*.pdf")
