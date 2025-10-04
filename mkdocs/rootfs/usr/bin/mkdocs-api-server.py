#!/usr/bin/env python3
"""
Simple HTTP API server for MkDocs operations
"""
import json
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MkDocsAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format_string, *args):
        """Override to use our logger"""
        logger.info(format_string % args)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/status':
            self.send_json_response({'status': 'ok', 'message': 'MkDocs API is running'})
        elif parsed_path.path == '/health':
            self.send_json_response({'status': 'healthy'})
        else:
            self.send_json_response({'status': 'error', 'message': 'Unknown endpoint'}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/rebuild':
            self.handle_rebuild()
        elif parsed_path.path == '/webhook':
            self.handle_webhook()
        else:
            self.send_json_response({'status': 'error', 'message': 'Unknown endpoint'}, 404)
    
    def handle_rebuild(self):
        """Handle rebuild request"""
        logger.info("Received rebuild request via API")
        
        # Start rebuild in background
        def run_rebuild():
            try:
                subprocess.run(['/usr/bin/mkdocs-rebuild'], check=True)
                logger.info("MkDocs rebuild completed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"MkDocs rebuild failed: {e}")
        
        threading.Thread(target=run_rebuild, daemon=True).start()
        
        self.send_json_response({
            'status': 'success', 
            'message': 'MkDocs rebuild started',
            'timestamp': int(time.time())
        })
    
    def handle_webhook(self):
        """Handle webhook request (same as rebuild for now)"""
        logger.info("Received webhook request")
        self.handle_rebuild()
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))

def run_server():
    """Run the HTTP server"""
    port = 8081
    server_address = ('', port)
    
    httpd = HTTPServer(server_address, MkDocsAPIHandler)
    logger.info(f"MkDocs API server starting on port {port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        httpd.server_close()

if __name__ == '__main__':
    run_server()