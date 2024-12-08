import os
import shutil
from pathlib import Path

# Font directory
font_dir = os.path.expanduser('~/Library/Fonts')

# Source and destination paths
source = os.path.join(font_dir, 'ComicNeue-Regular.ttf')
dest = os.path.join(font_dir, 'Comic Neue.ttf')

# Copy the Regular version as Comic Neue.ttf
if os.path.exists(source):
    # Remove existing corrupted file if it exists
    if os.path.exists(dest):
        os.remove(dest)
    # Copy the Regular version
    shutil.copy2(source, dest)
    print(f"Successfully created {dest}")
    
    # Verify the file size
    size = os.path.getsize(dest)
    print(f"New file size: {size} bytes")
else:
    print(f"Error: Could not find {source}")
