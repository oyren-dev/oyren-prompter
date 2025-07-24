# src/file_prompter/app.py

import os
import sys
from flask import Flask
try:
    import pkg_resources
    base_path = pkg_resources.resource_filename('file_prompter', '')
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    if not os.path.isdir(template_folder):
         print("Warning: pkg_resources template path not found. Falling back.", file=sys.stderr)
         template_folder = os.path.join(os.path.dirname(__file__), 'templates')
         static_folder = os.path.join(os.path.dirname(__file__), 'static')
except Exception as e:
     print(f"Warning: Error finding paths via pkg_resources ({e}). Using fallback.", file=sys.stderr)
     template_folder = os.path.join(os.path.dirname(__file__), 'templates')
     static_folder = os.path.join(os.path.dirname(__file__), 'static')

try:
    from .routes import setup_routes
except ImportError:
    # Handle direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from routes import setup_routes

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = os.urandom(24)

# Allow BASE_DIR to be configured via environment variable (useful for Docker)
BASE_DIR = os.environ.get('WORKSPACE_DIR', os.path.abspath(os.getcwd()))

# Setup routes
setup_routes(app, BASE_DIR)

def run_server():
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    print(f"--- Oyren Prompter ---")
    print(f"--- Serving files from: {BASE_DIR}")
    print(f"--- Static files from: {static_folder}")
    print(f"--- Access in browser: http://127.0.0.1:{port}")
    print("--- (Press CTRL+C to stop) ---")
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n--- Server stopped ---")
        sys.exit(0)
    except Exception as e:
        print(f"\n--- Server failed to start: {e} ---", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    print("[DEVELOPMENT MODE]")
    print(f"Base Directory (CWD): {BASE_DIR}")
    print(f"Template Folder: {template_folder}")
    print(f"Static Folder: {static_folder}")
    print("Run `python src/file_prompter/app.py` from your project root.")
    print(f"Access: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)