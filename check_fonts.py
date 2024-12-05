import matplotlib.font_manager as fm
import matplotlib as mpl

# Force a rebuild of the font cache
mpl.font_manager._load_fontmanager(try_read_cache=False)

# Get all available fonts
fonts = [f.name for f in fm.fontManager.ttflist]

print("Available fonts with 'Comic' in the name:")
comic_fonts = [f for f in fonts if 'comic' in f.lower()]
for font in comic_fonts:
    print(f"- {font}")

print("\nAvailable fonts with 'xkcd' in the name:")
xkcd_fonts = [f for f in fonts if 'xkcd' in f.lower()]
for font in xkcd_fonts:
    print(f"- {font}")

print("\nChecking specific font paths:")
for font in fm.fontManager.ttflist:
    if any(name in font.name.lower() for name in ['comic', 'xkcd']):
        print(f"{font.name}: {font.fname}")
