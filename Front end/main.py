# python file using pywebview to create a desktop app

import webview
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import time

def start_web_server():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_folder)
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

def main():
    
    # Start the web server
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    
    # Create the desktop window
    webview.create_window(
        'Innovative Leveling Tasks Manager',
        'http://localhost:8000/index.html', 
        height=900,
        min_size=(600, 700),# Minimum size
        resizable=True# Allow user to resize
    )
    
    # Show the window
    webview.start(debug=False)
    
if __name__ == '__main__':
    main()
