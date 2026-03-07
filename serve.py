#!/usr/bin/env python3
"""Simple HTTP server for testing the Puritan Gold PWA."""
import http.server
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Serving Puritan Gold at http://localhost:8080/app/")
print("Press Ctrl+C to stop")
http.server.HTTPServer(("", 8080), http.server.SimpleHTTPRequestHandler).serve_forever()
