#!/usr/bin/env bash
set -e

# Change directory to script directory
cd "$(dirname "$0")"

echo "===================================================="
echo " Building NotePad for macOS (Apple Silicon arm64)"
echo "===================================================="

# Determine Python command
PYTHON=""
if command -v python3.12 >/dev/null 2>&1; then
    PYTHON="python3.12"
elif [ -f "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" ]; then
    PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "Error: Python 3 is not found."
    exit 1
fi

echo "Using Python: $($PYTHON --version) at $(which $PYTHON)"

# Ensure PyInstaller is installed
if ! $PYTHON -m PyInstaller --version >/dev/null 2>&1; then
    echo "PyInstaller not found. Installing..."
    $PYTHON -m pip install pyinstaller
fi

# Ensure .icns exists
if [ ! -f "resources/app_icon.icns" ]; then
    echo "Generating resources/app_icon.icns..."
    $PYTHON -c "
import os
from PIL import Image
src = Image.open('resources/_app_icon.ico')
os.makedirs('resources/app_icon.iconset', exist_ok=True)
sizes = [
    ('icon_16x16.png', 16),
    ('icon_16x16@2x.png', 32),
    ('icon_32x32.png', 32),
    ('icon_32x32@2x.png', 64),
    ('icon_128x128.png', 128),
    ('icon_128x128@2x.png', 256),
    ('icon_256x256.png', 256),
    ('icon_256x256@2x.png', 512),
    ('icon_512x512.png', 512),
    ('icon_512x512@2x.png', 1024),
]
for name, s in sizes:
    resized = src.resize((s, s), Image.Resampling.LANCZOS)
    resized.save(os.path.join('resources/app_icon.iconset', name), 'PNG')
"
    iconutil -c icns resources/app_icon.iconset -o resources/app_icon.icns
    rm -rf resources/app_icon.iconset
fi

echo "Building NotePad.app with PyInstaller..."
$PYTHON -m PyInstaller --clean --noconfirm NotePad.spec

APP_PATH="dist/NotePad.app"
if [ ! -d "$APP_PATH" ]; then
    echo "Error: $APP_PATH was not generated!"
    exit 1
fi

echo "Signing NotePad.app bundle..."
xattr -cr "$APP_PATH"
codesign --force --deep --sign - "$APP_PATH" || echo "Warning: codesign failed, continuing..."

echo "Creating DMG package..."
DMG_NAME="NotePad-macOS-arm64.dmg"
DMG_PATH="dist/$DMG_NAME"
DMG_TMP="dist/dmg_tmp"

rm -rf "$DMG_PATH" "$DMG_TMP"
mkdir -p "$DMG_TMP"

# Copy App to DMG staging
cp -R "$APP_PATH" "$DMG_TMP/"

# Create symlink to /Applications for drag-and-drop install
ln -s /Applications "$DMG_TMP/Applications"

# Optional background or volume icon setup can be placed here
hdiutil create \
    -volname "NotePad" \
    -srcfolder "$DMG_TMP" \
    -ov \
    -format UDZO \
    "$DMG_PATH"

rm -rf "$DMG_TMP"

echo "===================================================="
echo " Build successful!"
echo " macOS Application: $APP_PATH"
echo " macOS DMG Image:   $DMG_PATH ($(du -sh "$DMG_PATH" | cut -f1))"
echo "===================================================="
