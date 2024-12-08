import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Test different relative differences
differences = [0.1, 0.01, 0.001, 0.0001, 0.00001]  # 10% down to 0.001%
n_tests = len(differences)

# Create a plot for each difference scale
fig, axes = plt.subplots(n_tests, 1, figsize=(8, 3*n_tests))
fig.suptitle('Testing PDF rendering with different relative differences')

for ax, diff in zip(axes, differences):
    # Create data with specified relative difference
    base = 4.385  # Similar to original data
    values = [base + i*base*diff for i in range(5)]
    labels = [f"Val {i+1}" for i in range(5)]
    
    # Calculate relative range as percentage
    rel_range = (max(values) - min(values)) / np.mean(values) * 100
    
    # Create bar plot
    ax.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax.set_yscale('log')
    
    # Print and display information
    trans = ax.transData.get_matrix()
    max_trans = np.max(np.abs(trans))
    title = f'Relative diff: {diff*100:.3f}% (range: {rel_range:.3f}%)'
    ax.set_title(title)
    print(f"\n{title}")
    print(f"Values: {values}")
    print(f"Transform matrix:\n{trans}")
    
    # Try both with and without explicit limits
    if diff == differences[-1]:  # For smallest difference, create two versions
        ax.set_ylim(min(values), max(values))
        print("Set explicit limits for smallest difference")

plt.tight_layout()

# Save with different settings
plt.savefig('differences_test_default.pdf')
plt.savefig('differences_test.png')

# Create a version with different figure sizes
with PdfPages('differences_test_sizes.pdf') as pdf:
    # Original size
    plt.savefig(pdf, format='pdf')
    
    # Double size
    fig.set_size_inches(16, 6*n_tests)
    plt.savefig(pdf, format='pdf')
    
    # Original size but higher DPI
    fig.set_size_inches(8, 3*n_tests)
    plt.savefig(pdf, format='pdf', dpi=600)

print("\nFiles saved as differences_test_default.pdf, differences_test.png, and differences_test_sizes.pdf")
plt.show()
