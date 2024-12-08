import matplotlib.font_manager as fm
import matplotlib as mpl
import os

# Add the correctly named font
font_path = os.path.expanduser('~/Library/Fonts/Comic Neue.ttf')
fm.fontManager.addfont(font_path)

# Rebuild the font cache
mpl.font_manager._load_fontmanager(try_read_cache=False)

# Verify the font is available
print("\nAvailable fonts:")
fonts = [f.name for f in fm.fontManager.ttflist if 'comic' in f.name.lower()]
print(fonts)