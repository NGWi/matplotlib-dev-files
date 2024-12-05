import matplotlib.pyplot as plt

# Create data
categories = ['A', 'B', 'C', 'D']
values = [3, 7, 2, 5]

# Create bar plot
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(categories, values)

# Add some styling
ax.set_title('Bar Plot Test')
ax.set_ylabel('Values')

# First display the plot
plt.show()

# Then save as PDF
fig.savefig('test_bars.pdf')

# Also save as PNG for comparison
fig.savefig('test_bars.png')