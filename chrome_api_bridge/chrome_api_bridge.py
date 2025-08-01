#!/usr/bin/env python3
"""
Native Messaging Host for Chrome API Bridge
This script acts as a bridge between HTTP requests on port 7444 and Chrome extension
"""

import sys
import json
import struct
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/chrome_bridge.log'),
        logging.StreamHandler()
    ]
)

class ChromeNativeMessaging:
    def __init__(self):
        self.pending_requests = {}
        self.message_thread = None
        self.http_server = None
        
    def send_message(self, message):
        """Send message to Chrome extension"""
        try:
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
            message_length = len(message_bytes)
            
            # Native messaging protocol: 4-byte length + message
            sys.stdout.buffer.write(struct.pack('<I', message_length))
            sys.stdout.buffer.write(message_bytes)
            sys.stdout.buffer.flush()
            
            logging.info(f"Sent message to extension: {message}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
    
    def read_message(self):
        """Read message from Chrome extension"""
        try:
            # Read message length (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length:
                return None
            
            message_length = struct.unpack('<I', raw_length)[0]
            
            # Read message
            raw_message = sys.stdin.buffer.read(message_length)
            if not raw_message:
                return None
            
            message = json.loads(raw_message.decode('utf-8'))
            logging.info(f"Received message from extension: {message}")
            return message
            
        except Exception as e:
            logging.error(f"Error reading message: {e}")
            return None
    
    def handle_chrome_messages(self):
        """Handle messages from Chrome extension"""
        while True:
            try:
                message = self.read_message()
                if message is None:
                    break
                
                # Handle response from extension
                if 'id' in message:
                    request_id = message['id']
                    if request_id in self.pending_requests:
                        self.pending_requests[request_id]['response'] = message
                        self.pending_requests[request_id]['event'].set()
                        
            except Exception as e:
                logging.error(f"Error in message handling: {e}")
                break
    
    def execute_chrome_command(self, command, params=None, timeout=10):
        """Execute Chrome API command and wait for response"""
        request_id = str(uuid.uuid4())
        
        # Create event for waiting
        import threading
        event = threading.Event()
        self.pending_requests[request_id] = {
            'event': event,
            'response': None
        }
        
        # Send command to extension
        message = {
            'id': request_id,
            'command': command,
            'params': params or {}
        }
        
        self.send_message(message)
        
        # Wait for response
        if event.wait(timeout):
            response = self.pending_requests[request_id]['response']
            del self.pending_requests[request_id]
            return response
        else:
            del self.pending_requests[request_id]
            return {'success': False, 'error': 'Timeout waiting for response'}

# HTTP Server to handle REST API requests
class ChromeAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, native_messaging=None, **kwargs):
        self.native_messaging = native_messaging
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                self.send_error(400, "Invalid API path")
                return
            
            # Parse command from URL: /chrome/tabs/query -> chrome.tabs.query
            if path_parts[0] == 'chrome':
                command = '.'.join(path_parts[1:])
                
                # Parse query parameters
                params = {}
                if parsed_url.query:
                    query_params = parse_qs(parsed_url.query)
                    for key, value in query_params.items():
                        params[key] = value[0] if len(value) == 1 else value
                
                # Execute command
                response = self.native_messaging.execute_chrome_command(command, params)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_error(404, "Not found")
                
        except Exception as e:
            logging.error(f"Error handling GET: {e}")
            self.send_error(500, str(e))
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                self.send_error(400, "Invalid API path")
                return
            
            # Parse command from URL
            if path_parts[0] == 'chrome':
                command = '.'.join(path_parts[1:])
                
                # Parse JSON body
                params = {}
                if post_data:
                    try:
                        params = json.loads(post_data.decode('utf-8'))
                    except json.JSONDecodeError:
                        self.send_error(400, "Invalid JSON in request body")
                        return
                
                # Execute command
                response = self.native_messaging.execute_chrome_command(command, params)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_error(404, "Not found")
                
        except Exception as e:
            logging.error(f"Error handling POST: {e}")
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests (CORS)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logging.info(f"HTTP: {format % args}")

def create_handler(native_messaging):
    """Create HTTP handler with native messaging instance"""
    def handler(*args, **kwargs):
        ChromeAPIHandler(*args, native_messaging=native_messaging, **kwargs)
    return handler

def main():
    logging.info("Starting Chrome API Bridge Native Host")
    
    # Create native messaging instance
    native_messaging = ChromeNativeMessaging()
    
    # Start message handling thread
    message_thread = threading.Thread(target=native_messaging.handle_chrome_messages)
    message_thread.daemon = True
    message_thread.start()
    
    # Start HTTP server
    handler_class = create_handler(native_messaging)
    httpd = HTTPServer(('localhost', 7444), handler_class)
    
    logging.info("HTTP server listening on port 7444")
    logging.info("Ready to receive Chrome API commands")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        httpd.shutdown()

if __name__ == '__main__':
    main()
