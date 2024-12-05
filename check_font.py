import os
from pathlib import Path

# Font directory
font_dir = os.path.expanduser('~/Library/Fonts')

# List all files in the font directory
print("Checking font directory contents:")
font_files = list(Path(font_dir).glob('Comic*.ttf'))
for file in font_files:
    print(f"Found: {file.name}")
    # Check if file is readable
    try:
        with open(file, 'rb') as f:
            # Try to read first few bytes
            f.read(10)
        print(f"File is readable")
    except Exception as e:
        print(f"Error reading file: {e}")

# Also check file permissions
for file in font_files:
    stat = file.stat()
    print(f"\nPermissions for {file.name}:")
    print(f"Mode: {oct(stat.st_mode)}")
    print(f"Owner: {stat.st_uid}")
    print(f"Group: {stat.st_gid}")
    print(f"Size: {stat.st_size} bytes")
