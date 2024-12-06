import matplotlib.pyplot as plt
import numpy as np

# Data
y_values = [4.385236951214598, 4.385249349505862, 4.38524255048674,
            4.385237751115038, 4.385241350648787]
x_labels = ["Dota", "Youtube", "Exchange", "Fifa", "Uber"]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Fix color mapping to use proper [0,1] range
# colors = plt.cm.viridis(np.linspace(0, 1, len(x_labels))) # Unnecessary change
ax.bar(x_labels, y_values, color=plt.cm.viridis(range(len(x_labels))))

ax.set_yscale('log')
"""Set y-axis to log scale with explicit limits to show the small differences.
Hypothesis: By default, matplotlib tries to set "nice" axis limits that round to nearby numbers.
With log scale and very small differences (here only ~0.0012% relative difference),
the default limits end up making the bars invisible.
Setting explicit tight limits forces matplotlib to show the full range of the data"""
ax.set_ylim(min(y_values) * 0.9999, max(y_values) * 1.0001) # Fix for issue

# Add title and labels
ax.set_title("Contracts vs. Values (Log Scale)")
ax.set_xlabel("Contracts")
ax.set_ylabel("Values")

# Save the plot as a PDF file
fig.savefig('gas-burnt-per-contract.pdf', dpi=300, bbox_inches='tight',
            transparent=True, pad_inches=0)

# Display the plot
plt.show()