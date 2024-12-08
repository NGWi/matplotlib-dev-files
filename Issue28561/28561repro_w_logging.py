import matplotlib.pyplot as plt
import numpy as np

# Data
y_values = [4.385236951214598, 4.385249349505862, 4.38524255048674, 4.385237751115038, 4.385241350648787]
x_labels = ["Dota", "Youtube", "Exchange", "Fifa", "Uber"]

# Print data range info for debugging
print(f"Y-value range: {max(y_values) - min(y_values)}")
print(f"Y-value relative range: {(max(y_values) - min(y_values)) / np.mean(y_values)}")

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Fix color mapping to use proper range
colors = plt.cm.viridis(np.linspace(0, 1, len(x_labels)))
print("Color values:", colors)  # Debug color values

bars = ax.bar(x_labels, y_values, color=colors)

# Set y-axis to log scale with explicit limits
ax.set_yscale('log')
# Set limits to show the small differences
ax.set_ylim(min(y_values) * 0.9999, max(y_values) * 1.0001)

# Add title and labels
ax.set_title("Contracts vs. Values (Log Scale)")
ax.set_xlabel("Contracts")
ax.set_ylabel("Values")

# Save versions with different settings for comparison
# 1. Original problematic version
fig.savefig('gas-burnt-per-contract-transparent.pdf', dpi=300, bbox_inches='tight', transparent=True, pad_inches=0)

# 2. Non-transparent version
fig.savefig('gas-burnt-per-contract-solid.pdf', dpi=300, bbox_inches='tight', transparent=False)

# 3. Version with explicit backend
plt.savefig('gas-burnt-per-contract-backend.pdf', dpi=300, bbox_inches='tight', 
            transparent=False, backend='pdf')

# Display the plot
plt.show()