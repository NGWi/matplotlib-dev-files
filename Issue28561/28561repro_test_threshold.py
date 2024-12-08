import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Create test data with different scales
scales = [1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6]
n_scales = len(scales)

# Create a plot for each scale
fig, axes = plt.subplots(n_scales, 1, figsize=(8, 3*n_scales))
fig.suptitle('Testing PDF rendering threshold with log scale')

for ax, scale in zip(axes, scales):
    # Create data with relative differences at different scales
    base = 1000 * scale
    values = [base + i*base*0.001 for i in range(5)]  # 0.1% differences
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Create bar plot
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    # Print transform info
    trans = ax.transData.get_matrix()
    max_trans = np.max(np.abs(trans))
    ax.set_title(f'Scale {scale:.0e}, Max transform: {max_trans:.2e}')
    print(f"\nScale {scale:.0e}:")
    print(f"Data range: {min(values):.2e} to {max(values):.2e}")
    print(f"Transform matrix:\n{trans}")

plt.tight_layout()

# Save as PDF and PNG for comparison
plt.savefig('threshold_test.pdf')
plt.savefig('threshold_test.png')

print("\nFiles saved as threshold_test.pdf and threshold_test.png")
print("Compare the PDF and PNG to see at which scale the bars disappear")

plt.show()
