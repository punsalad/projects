#!/bin/bash

# Chrome API Bridge Installation Script

echo "Installing Chrome API Bridge..."

# 1. Copy the Python script to /usr/local/bin
sudo cp chrome_api_bridge.py /usr/local/bin/
sudo chmod +x /usr/local/bin/chrome_api_bridge.py

# 2. Create native messaging host directory
NATIVE_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
mkdir -p "$NATIVE_DIR"

# 3. Get extension ID (you'll need to replace this with your actual extension ID)
echo "Please enter your Chrome extension ID:"
read EXTENSION_ID

# 4. Create the native messaging host manifest
cat > "$NATIVE_DIR/com.chrome.api.bridge.json" << EOF
{
  "name": "com.chrome.api.bridge",
  "description": "Chrome API Bridge Native Host",
  "path": "/usr/local/bin/chrome_api_bridge.py",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://$EXTENSION_ID/"
  ]
}
