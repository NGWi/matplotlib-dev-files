import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Data
y_values = [4.385236951214598, 4.385249349505862, 4.38524255048674,
            4.385237751115038, 4.385241350648787]
x_labels = ["Dota", "Youtube", "Exchange", "Fifa", "Uber"]

def create_plot(ax, set_limits=False):
    """Create the bar plot with optional limit setting"""
    bars = ax.bar(x_labels, y_values, color=plt.cm.viridis(range(len(x_labels))))
    ax.set_yscale('log')
    if set_limits:
        ax.set_ylim(min(y_values), max(y_values))
    
    ax.set_title("Contracts vs. Values (Log Scale)")
    ax.set_xlabel("Contracts")
    ax.set_ylabel("Values")
    return bars

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# First plot: without explicit limits
bars1 = create_plot(ax1, set_limits=False)
ax1.set_title("Without explicit limits")

# Second plot: with explicit limits
bars2 = create_plot(ax2, set_limits=True)
ax2.set_title("With explicit limits")

# Print debugging information
print("Backend information:")
print(f"Current backend: {plt.get_backend()}")
print(f"Available PDF backends: {[b for b in plt.rcsetup.all_backends if 'pdf' in b.lower()]}")

# Print transformation information
print("\nCoordinate transformation info:")
for ax, name in [(ax1, "Without limits"), (ax2, "With limits")]:
    print(f"\n{name}:")
    print(f"Y-axis limits: {ax.get_ylim()}")
    print(f"Y-axis scale: {ax.get_yscale()}")
    # Get the transformation pipeline
    trans = ax.transData
    print(f"Transform bounds: {trans.get_matrix()}")
    
    # Print actual bar heights in display coordinates
    for bar in (bars1 if ax == ax1 else bars2):
        bbox = bar.get_window_extent()
        print(f"Bar height in display coords: {bbox.height}")

# Save with different backends/formats
backends_to_test = {
    'pdf': 'output_default.pdf',
    'png': 'output_agg.png',
    'svg': 'output_svg.svg',
    'ps': 'output_ps.ps'
}

for fmt, filename in backends_to_test.items():
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nSaved {fmt.upper()} output to {filename}")

# Create a multi-page PDF to test different PDF settings
with PdfPages('output_pdf_tests.pdf') as pdf:
    # Test 1: Default settings
    plt.savefig(pdf, format='pdf', dpi=300)
    
    # Test 2: Without bbox_inches
    plt.savefig(pdf, format='pdf', dpi=300, bbox_inches=None)
    
    # Test 3: With different DPI
    plt.savefig(pdf, format='pdf', dpi=600)
    
    # Test 4: With metadata
    plt.savefig(pdf, format='pdf', dpi=300, metadata={'CreationDate': None})

print("\nCreated multi-page PDF with different settings in output_pdf_tests.pdf")

# Display the plot
plt.show()
