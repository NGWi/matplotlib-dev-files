import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Data
y_values = [4.385236951214598, 4.385249349505862, 4.38524255048674,
            4.385237751115038, 4.385241350648787]
x_labels = ["Dota", "Youtube", "Exchange", "Fifa", "Uber"]

# Create figure with multiple test cases
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Test 1: Original data with default settings
ax1.bar(x_labels, y_values, color=plt.cm.viridis(range(len(x_labels))))
ax1.set_yscale('log')
ax1.set_title("Original (log scale)")
print("Test 1 transform:", ax1.transData.get_matrix())

# Test 2: Scale data to [0,1] range
y_min, y_max = min(y_values), max(y_values)
y_scaled = [(y - y_min)/(y_max - y_min) for y in y_values]
ax2.bar(x_labels, y_scaled, color=plt.cm.viridis(range(len(x_labels))))
ax2.set_yscale('log')
ax2.set_title("Scaled to [0,1] (log scale)")
print("Test 2 transform:", ax2.transData.get_matrix())

# Test 3: Linear scale with original data
ax3.bar(x_labels, y_values, color=plt.cm.viridis(range(len(x_labels))))
ax3.set_title("Original (linear scale)")
print("Test 3 transform:", ax3.transData.get_matrix())

# Test 4: Offset data to start at 1
y_offset = [y - y_min + 1 for y in y_values]
ax4.bar(x_labels, y_offset, color=plt.cm.viridis(range(len(x_labels))))
ax4.set_yscale('log')
ax4.set_title("Offset to start at 1 (log scale)")
print("Test 4 transform:", ax4.transData.get_matrix())

# Print the actual data ranges
print("\nData ranges:")
print(f"Original: {max(y_values) - min(y_values)}")
print(f"Scaled: {max(y_scaled) - min(y_scaled)}")
print(f"Offset: {max(y_offset) - min(y_offset)}")

# Save with different settings
plt.savefig('scaling_test_default.pdf')
plt.savefig('scaling_test.png')  # For comparison

# Try different scales for PDF output
with PdfPages('scaling_tests.pdf') as pdf:
    # Default
    plt.savefig(pdf, format='pdf')
    
    # Try adjusting figure size
    fig.set_size_inches(30, 24)
    plt.savefig(pdf, format='pdf')
    
    # Reset size and try different DPI
    fig.set_size_inches(15, 12)
    plt.savefig(pdf, format='pdf', dpi=600)

plt.show()
