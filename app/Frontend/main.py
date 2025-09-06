# python file using pywebview to create a desktop app
# 2025 bryan paul - Updated to use PyWebView API bridge instead of HTTP server
import webview
import os
from api import TaskAPI  # Import our API bridge class

def main():
    # Get current directory for serving static files
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Create API instance that will be exposed to JavaScript
    api = TaskAPI()
    
    # Create the desktop window with API bridge
    # js_api parameter exposes Python methods to JavaScript via pywebview.api
    webview.create_window(
        'Innovative Leveling Tasks Manager',
        os.path.join(current_folder, 'index.html'),  # Serve file directly, no HTTP server needed
        js_api=api,  # Expose TaskAPI methods to JavaScript
        height=900,
        min_size=(600, 700),
        resizable=True
    )
    
    # Show the window
    webview.start(debug=False)
    
if __name__ == '__main__':
    main()
