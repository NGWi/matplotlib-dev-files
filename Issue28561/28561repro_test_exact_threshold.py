import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test a finer range of differences around the threshold
differences = [
    0.00005,    # 0.005%   - Should work
    0.00002,    # 0.002%   - Should work
    0.00001,    # 0.001%   - Should work
    0.000005,   # 0.0005%  - Might fail
    0.000002,   # 0.0002%  - Might fail
    0.000001    # 0.0001%  - Should fail
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
plt.savefig('exact_threshold_test.pdf')
plt.savefig('exact_threshold_test.png')  # For comparison

print("\nFiles saved as exact_threshold_test.pdf and exact_threshold_test.png")
print("Compare to find exact threshold where bars disappear")

plt.show()
