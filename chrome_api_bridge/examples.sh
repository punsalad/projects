#!/bin/bash

# Chrome API Bridge - Usage Examples

echo "Chrome API Bridge - Usage Examples"
echo "=================================="

# Start the native host (the extension will launch it automatically)
# But you can also run it manually for testing:
# python3 /usr/local/bin/chrome_api_bridge.py

echo ""
echo "===== TAB OPERATIONS ====="

echo "# Create a new tab"
echo "curl -X POST http://localhost:7444/chrome/tabs/create \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"url\": \"https://example.com\"}'"
echo ""

echo "# Get all tabs"
echo "curl http://localhost:7444/chrome/tabs/query"
echo ""

echo "# Get active tab"
echo "curl \"http://localhost:7444/chrome/tabs/query?active=true&currentWindow=true\""
echo ""

echo "# Update a tab URL"
echo "curl -X POST http://localhost:7444/chrome/tabs/update \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"tabId\": 123, \"updateProperties\": {\"url\": \"https://google.com\"}}'"
echo ""

echo "# Close a tab"
echo "curl -X POST http://localhost:7444/chrome/tabs/close \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"tabId\": 123}'"
echo ""

echo "===== BOOKMARK OPERATIONS ====="

echo "# Create a bookmark"
echo "curl -X POST http://localhost:7444/chrome/bookmarks/create \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"title\": \"Example Site\", \"url\": \"https://example.com\"}'"
echo ""

echo "# Search bookmarks"
echo "curl -X POST http://localhost:7444/chrome/bookmarks/search \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"query\": \"example\"}'"
echo ""

echo "# Get bookmark tree"
echo "curl http://localhost:7444/chrome/bookmarks/getTree"
echo ""

echo "===== WINDOW OPERATIONS ====="

echo "# Create a new window"
echo "curl -X POST http://localhost:7444/chrome/windows/create \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"url\": \"https://example.com\", \"width\": 800, \"height\": 600}'"
echo ""

echo "# Get all windows"
echo "curl http://localhost:7444/chrome/windows/getAll"
echo ""

echo "# Get current window"
echo "curl http://localhost:7444/chrome/windows/getCurrent"
echo ""

echo "===== STORAGE OPERATIONS ====="

echo "# Store data"
echo "curl -X POST http://localhost:7444/chrome/storage/set \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"items\": {\"key1\": \"value1\", \"key2\": \"value2\"}}'"
echo ""

echo "# Get data"
echo "curl -X POST http://localhost:7444/chrome/storage/get \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"keys\": [\"key1\", \"key2\"]}'"
