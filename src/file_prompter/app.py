# src/file_prompter/app.py

import os
import sys
# Make sure jsonify and json are imported
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
# (Keep pkg_resources import and template/static folder logic)
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

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = os.urandom(24)
BASE_DIR = os.path.abspath(os.getcwd())

# --- Helper Functions (is_safe_path, get_directory_contents - Keep As Is) ---
def is_safe_path(path_to_check):
    try:
        abs_path = os.path.abspath(path_to_check)
        return os.path.commonpath([BASE_DIR, abs_path]) == BASE_DIR
    except ValueError:
        return False

def get_directory_contents(relative_path=""):
    # (Keep the existing code for this function)
    clean_relative_path = relative_path.strip('/')
    current_abs_path = os.path.join(BASE_DIR, clean_relative_path)
    if not is_safe_path(current_abs_path):
        return [], [], f"Access denied: Path '{relative_path}' is outside the base directory."
    if not os.path.isdir(current_abs_path):
         return [], [], f"Error: Path '{relative_path}' is not a valid directory."
    try:
        items = os.listdir(current_abs_path)
    except OSError as e:
        return [], [], f"Error listing directory '{relative_path}': {e}"
    directories = []
    files = []
    for item in sorted(items, key=str.lower):
        item_abs_path = os.path.join(current_abs_path, item)
        item_rel_path = os.path.relpath(item_abs_path, BASE_DIR)
        item_rel_path_norm = item_rel_path.replace(os.sep, '/')
        try:
            if os.path.isdir(item_abs_path):
                directories.append({"name": item, "rel_path": item_rel_path_norm})
            elif os.path.isfile(item_abs_path):
                 files.append({"name": item, "rel_path": item_rel_path_norm})
        except OSError:
             print(f"Warning: Could not access item '{item}' in '{relative_path}'. Skipping.", file=sys.stderr)
             continue
    return directories, files, None


# --- Flask Routes ---

# (browse route - Keep As Is)
@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse(path=""):
    relative_path = path.strip('/')
    directories, files, error = get_directory_contents(relative_path)
    parent_path = None
    if relative_path:
        parent_dir = os.path.dirname(relative_path)
        parent_path = parent_dir if parent_dir else ""
        parent_path = parent_path.replace(os.sep, '/')
    if error:
        flash(error, 'error')
    return render_template(
        'browser.html',
        current_relative_path=relative_path.replace(os.sep, '/'),
        parent_path=parent_path,
        directories=directories,
        files=files
    )


# (preview_content route - Keep As Is)
@app.route('/preview_content', methods=['POST'])
def preview_content():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    selected_files_rel_paths = data.get('selected_files', [])
    if not isinstance(selected_files_rel_paths, list):
         return jsonify({"error": "Invalid data format"}), 400
    preview_content_parts = []
    errors_encountered = []
    for rel_path in selected_files_rel_paths:
        abs_path = os.path.join(BASE_DIR, rel_path.strip('/'))
        if not is_safe_path(abs_path) or not os.path.isfile(abs_path):
            error_msg = f"Skipped invalid/unsafe file for preview: {rel_path}"
            errors_encountered.append(error_msg)
            continue
        try:
            preview_content_parts.append(f"--- Preview from: {rel_path} ---\n")
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                preview_content_parts.append(content)
            preview_content_parts.append("\n--- End Preview ---\n")
        except Exception as e:
            error_msg = f"Error reading file '{rel_path}' for preview: {e}"
            errors_encountered.append(error_msg)
    full_preview = "\n".join(preview_content_parts).strip()
    return jsonify({
        "preview_content": full_preview,
        "errors": errors_encountered
    })


# *** MODIFIED: /process route now handles JSON request for final generation ***
@app.route('/process', methods=['POST'])
def process_files():
    """Handles AJAX request to generate final output and returns JSON."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    selected_files_rel_paths = data.get('selected_files', [])
    prompt = data.get('prompt', '').strip()

    if not isinstance(selected_files_rel_paths, list):
         return jsonify({"error": "Invalid selected_files format"}), 400
    if not isinstance(prompt, str):
        return jsonify({"error": "Invalid prompt format"}), 400

    # --- Concatenation Logic (same as before) ---
    concatenated_content_parts = []
    errors_encountered = []

    if prompt:
        concatenated_content_parts.append("--- User Prompt ---")
        concatenated_content_parts.append(prompt)
        concatenated_content_parts.append("--- End User Prompt ---")
        concatenated_content_parts.append("\n")

    if not selected_files_rel_paths and not prompt:
         # Allow generating just the prompt if no files selected? Or return error?
         # Let's return an error if nothing is to be generated.
         return jsonify({"final_output": "", "errors": ["No files selected and no prompt provided."]})


    for rel_path in selected_files_rel_paths:
        abs_path = os.path.join(BASE_DIR, rel_path.strip('/'))

        if not is_safe_path(abs_path) or not os.path.isfile(abs_path):
            error_msg = f"Security Denied or Invalid File: '{rel_path}'"
            print(f"Warning: {error_msg}", file=sys.stderr)
            errors_encountered.append(error_msg)
            continue

        try:
            concatenated_content_parts.append(f"--- Content from: {rel_path} ---")
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                concatenated_content_parts.append(content)
            concatenated_content_parts.append("--- End Content ---")
            concatenated_content_parts.append("\n")
        except Exception as e:
            error_msg = f"Error reading file '{rel_path}': {e}"
            print(error_msg, file=sys.stderr)
            errors_encountered.append(error_msg)

    final_output = "\n".join(concatenated_content_parts).strip()

    # *** Return JSON instead of rendering template ***
    return jsonify({
        "final_output": final_output,
        "errors": errors_encountered
    })

# (run_server and if __name__ == '__main__' blocks remain the same)
def run_server():
    print(f"--- Oyren Prompter ---")
    print(f"--- Serving files from: {BASE_DIR}")
    print(f"--- Static files from: {static_folder}")
    print(f"--- Access in browser: http://127.0.0.1:5000")
    print("--- (Press CTRL+C to stop) ---")
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n--- Server stopped ---")
        sys.exit(0)
    except Exception as e:
        print(f"\n--- Server failed to start: {e} ---", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    print("[DEVELOPMENT MODE]")
    print(f"Base Directory (CWD): {BASE_DIR}")
    print(f"Template Folder: {template_folder}")
    print(f"Static Folder: {static_folder}")
    print("Run `python src/oyren_prompter/app.py` from your project root.") # Adjust path if needed
    print("Access: http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)