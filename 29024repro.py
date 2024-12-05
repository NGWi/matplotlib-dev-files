import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(2, 2), dpi=int(240 / 2))

ax.set_aspect(1)
ax.set_xlim(0, 240)
ax.set_ylim(0, 240)

ax.axis("off")
ax.patch.set_visible(False)
ax.patch.set_alpha(0)

fig.patch.set_visible(False)
fig.patch.set_alpha(0)

ax.plot([], [])

def animate(frame):
    return ax.plot(range(10, frame), range(10, frame))

ani = FuncAnimation(fig, animate, frames=100, interval=3, blit=True, repeat=False)
ani.save('test.gif', writer='ffmpeg', savefig_kwargs=dict(transparent=True, facecolor='none'))
plt.show()

# Create an HTML file to test transparency
html_content = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    background: repeating-conic-gradient(#808080 0% 25%, #fff 0% 50%) 
                50% / 20px 20px;
}
img {
    display: block;
    margin: 50px auto;
    border: 1px solid black;
}
</style>
</head>
<body>
    <img src="test.gif">
</body>
</html>
"""

with open('test_transparency.html', 'w') as f:
    f.write(html_content)

print("Created test_transparency.html - open it in a browser to check if the GIF is truly transparent")