import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test very fine range around the threshold
differences = [
    0.000010,    # 0.0100% - Last working
    0.000009,    # 0.0090%
    0.000008,    # 0.0080%
    0.000007,    # 0.0070%
    0.000006,    # 0.0060%
    0.000005     # 0.00050% - First failing
]
n_tests = len(differences)

# Create a plot for each difference
fig, axes = plt.subplots(n_tests, 1, figsize=(8, 3*n_tests))
fig.suptitle('Finding exact threshold where PDF rendering fails')

for ax, diff in zip(axes, differences):
    # Create data with specified relative difference
    base = 4.385  # Same as original
    values = [base + i*base*diff for i in range(5)]
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Calculate relative range
    rel_range = (max(values) - min(values)) / np.mean(values) * 100
    
    # Create bar plot
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    # Get transformation info
    trans = ax.transData.get_matrix()
    max_trans = np.max(np.abs(trans))
    
    # Print and display information
    title = f'Diff: {diff*100:.4f}% (range: {rel_range:.4f}%), Max transform: {max_trans:.2e}'
    ax.set_title(title)
    print(f"\n{title}")
    print(f"Values: {values}")
    print(f"Transform matrix:\n{trans}")

plt.tight_layout()

# Save with different settings
plt.savefig('final_threshold_test.pdf')
plt.savefig('final_threshold_test.png')  # For comparison

print("\nFiles saved as final_threshold_test.pdf and final_threshold_test.png")
print("Compare to find exact threshold where bars disappear")

plt.show()
