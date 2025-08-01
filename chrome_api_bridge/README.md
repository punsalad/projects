# Chrome API Bridge

A Chrome extension that provides a command-line interface to Chrome APIs through Native Messaging.

## Features

- Control Chrome tabs, bookmarks, windows, and more from the command line
- HTTP REST API on port 7444
- Secure Native Messaging communication
- Support for all major Chrome APIs

## Installation

1. **Load the Chrome extension:**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension` folder

2. **Install the native host:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Get your extension ID:**
   - Copy the extension ID from the Chrome extensions page
   - Enter it when prompted by the install script

## Usage

```bash
# Create a new tab
curl -X POST http://localhost:7444/chrome/tabs/create -d '{"url": "https://example.com"}'

# Get all tabs
curl http://localhost:7444/chrome/tabs/query

# Create a bookmark
curl -X POST http://localhost:7444/chrome/bookmarks/create -d '{"title": "Example", "url": "https://example.com"}'
```

See `examples.sh` for more usage examples.

## Architecture

```
Command Line ←→ HTTP Server (7444) ←→ Native Host ←→ Chrome Extension ←→ Chrome APIs
```

## Files

- `extension/` - Chrome extension files
- `chrome_api_bridge.py` - Native messaging host
- `install.sh` - Installation script
- `examples.sh` - Usage examples
