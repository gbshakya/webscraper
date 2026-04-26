from http.server import BaseHTTPRequestHandler
from urllib import parse
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests"""
        try:
            # Parse the path and query parameters
            path = self.path
            query = dict(parse.parse_qsl(parse.urlsplit(path).query))
            
            # Simple routing
            if path == '/' or path == '':
                response_data = {
                    "message": "Nepal Stock Exchange Data API (Minimal)",
                    "version": "1.0",
                    "environment": "serverless",
                    "endpoints": {
                        "GET /": "API information",
                        "GET /health": "Health check",
                        "GET /symbols": "Get available symbols",
                        "GET /test": "Test endpoint"
                    }
                }
            elif path == '/health':
                response_data = {
                    "status": "healthy",
                    "message": "API is working!",
                    "path": path,
                    "query": query
                }
            elif path == '/symbols':
                response_data = {
                    "symbols": ["NABIL", "NIMB", "SCB", "HBL", "SBI", "EBL", "NICA", "MBL"],
                    "total": 8,
                    "source": "hardcoded_for_testing"
                }
            elif path == '/test':
                response_data = {
                    "message": "Test successful!",
                    "path": path,
                    "query_params": query,
                    "user_agent": self.headers.get('User-Agent', 'Unknown')
                }
            else:
                response_data = {
                    "error": "Endpoint not found",
                    "path": path,
                    "available_endpoints": ["/", "/health", "/symbols", "/test"]
                }
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                return
            
            # Send successful response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            # Send error response
            error_data = {
                "error": "Internal server error",
                "message": str(e),
                "path": self.path
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            response_data = {
                "message": "POST request received",
                "path": self.path,
                "headers": dict(self.headers),
                "body_length": content_length,
                "body": post_data.decode('utf-8', errors='ignore') if content_length > 0 else None
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            error_data = {
                "error": "Internal server error",
                "message": str(e),
                "path": self.path
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode())

# Export handler for Vercel
app = handler  # Vercel expects 'app' variable
application = handler  # Alternative name for some platforms
