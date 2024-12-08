import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test just the two critical cases with detailed matrix analysis
differences = [
    0.000010,    # 0.00100% - Fails
    0.000009,    # 0.00090% - Works
]

def analyze_transform(ax, title, values, labels):
    """Analyze transformation matrices in detail"""
    # Get all transform components
    trans_data = ax.transData.get_matrix()
    
    print(f"\n{title}")
    print("Data transform matrix:")
    print(trans_data)
    
    # Analyze each bar's position
    print("\nBar positions:")
    for label, value in zip(labels, values):
        # Get the transformed position of this bar
        display_pos = ax.transData.transform([[0, value]])[0]
        print(f"{label}: value={value:.8f}, y_transform={display_pos[1]:.2e}")
    
    # Calculate and print additional metrics
    print("\nMetrics:")
    print(f"Max value: {np.max(np.abs(trans_data)):.2e}")
    print(f"Min value: {np.min(np.abs(trans_data[trans_data != 0])):.2e}")
    print(f"Condition number: {np.linalg.cond(trans_data):.2e}")
    print(f"Value range: {max(values) - min(values):.2e}")
    print(f"Log10 range: {np.log10(max(values)) - np.log10(min(values)):.2e}")

# Create plots with detailed analysis
fig, axes = plt.subplots(len(differences), 1, figsize=(8, 4*len(differences)))
if len(differences) == 1:
    axes = [axes]

for ax, diff in zip(axes, differences):
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
    title = f'Diff: {diff*100:.4f}% (range: {rel_range:.4f}%)'
    ax.set_title(title)
    analyze_transform(ax, title, values, labels)

plt.tight_layout()

# Save with different settings
plt.savefig('matrix_analysis_test.pdf')
plt.savefig('matrix_analysis_test.png')

print("\nFiles saved as matrix_analysis_test.pdf and matrix_analysis_test.png")
plt.show()
