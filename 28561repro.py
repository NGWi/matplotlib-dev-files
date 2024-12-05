import matplotlib.pyplot as plt

# Data
y_values = [4.385236951214598, 4.385249349505862, 4.38524255048674, 4.385237751115038, 4.385241350648787]
x_labels = ["Dota", "Youtube", "Exchange", "Fifa", "Uber"]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x_labels, y_values, color=plt.cm.viridis(range(len(x_labels))))

# Set y-axis to log scale
ax.set_yscale('log')

# Add title and labels
ax.set_title("Contracts vs. Values (Log Scale)")
ax.set_xlabel("Contracts")
ax.set_ylabel("Values")

# Save the plot as a PDF file
fig.savefig('gas-burnt-per-contract.pdf', dpi=300, bbox_inches='tight', transparent=True, pad_inches=0)

# Display the plot
plt.show()