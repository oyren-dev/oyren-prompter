# src/file_prompter/app.py

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify # Added jsonify
import json # Added json for parsing request data

# --- Package-aware Template Finding ---
# (Keep the existing template finding logic using pkg_resources or fallback)
try:
    import pkg_resources
    # 'file_prompter' should match the package name defined in pyproject.toml
    base_path = pkg_resources.resource_filename('file_prompter', '')
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static') # Define static folder path
    if not os.path.isdir(template_folder):
         print("Warning: pkg_resources template path not found. Falling back.", file=sys.stderr)
         template_folder = os.path.join(os.path.dirname(__file__), 'templates')
         static_folder = os.path.join(os.path.dirname(__file__), 'static') # Fallback static path
except Exception as e:
     print(f"Warning: Error finding paths via pkg_resources ({e}). Using fallback.", file=sys.stderr)
     template_folder = os.path.join(os.path.dirname(__file__), 'templates')
     static_folder = os.path.join(os.path.dirname(__file__), 'static')


# --- Flask App Initialization ---
# Pass static_folder path to Flask constructor
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = os.urandom(24)

# --- CRITICAL: Base Directory for User Files ---
BASE_DIR = os.path.abspath(os.getcwd())


# --- Helper Functions ---
# (is_safe_path and get_directory_contents remain the same)
def is_safe_path(path_to_check):
    """
    Security check: Ensures the requested path is within the BASE_DIR.
    Prevents accessing files outside the intended working directory.
    """
    try:
        # Resolve the absolute path, normalizing '..' etc.
        abs_path = os.path.abspath(path_to_check)
        # Check if the common path of BASE_DIR and the resolved path starts
        # with BASE_DIR. This prevents navigating above BASE_DIR.
        return os.path.commonpath([BASE_DIR, abs_path]) == BASE_DIR
    except ValueError:
        # Can happen if paths are on different drives on Windows
        return False

def get_directory_contents(relative_path=""):
    """
    Lists directories and files in a given relative path within BASE_DIR.
    (Code is the same as previous version)
    """
    # Ensure relative_path doesn't start with '/' to avoid issues with os.path.join
    clean_relative_path = relative_path.strip('/')
    current_abs_path = os.path.join(BASE_DIR, clean_relative_path)

    if not is_safe_path(current_abs_path):
        msg = f"Access denied: Path '{relative_path}' is outside the base directory."
        print(f"Warning: {msg}", file=sys.stderr)
        return [], [], msg

    if not os.path.isdir(current_abs_path):
        msg = f"Error: Path '{relative_path}' is not a valid directory."
        print(f"Warning: {msg}", file=sys.stderr)
        return [], [], msg

    try:
        items = os.listdir(current_abs_path)
    except OSError as e:
        msg = f"Error listing directory '{relative_path}': {e}"
        print(msg, file=sys.stderr)
        return [], [], msg

    directories = []
    files = []
    for item in sorted(items, key=str.lower): # Sort case-insensitively
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
    return directories, files, None # No error

# --- Flask Routes ---

# (browse route remains the same)
@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse(path=""):
    # Normalize path input (remove trailing slashes, etc.)
    relative_path = path.strip('/')
    directories, files, error = get_directory_contents(relative_path)

    # Determine parent path for "Up" link
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


# *** NEW ROUTE FOR DYNAMIC CONTENT PREVIEW ***
@app.route('/preview_content', methods=['POST'])
def preview_content():
    """Fetches concatenated content for selected files for AJAX preview."""
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

        # Security check
        if not is_safe_path(abs_path) or not os.path.isfile(abs_path):
            error_msg = f"Skipped invalid/unsafe file for preview: {rel_path}"
            print(f"Warning: {error_msg}", file=sys.stderr)
            errors_encountered.append(error_msg)
            continue

        try:
            # Simple header for preview clarity
            preview_content_parts.append(f"--- Preview from: {rel_path} ---\n")
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Limit preview size per file if needed? For now, read all.
                content = f.read()
                preview_content_parts.append(content)
            preview_content_parts.append("\n--- End Preview ---\n")
        except Exception as e:
            error_msg = f"Error reading file '{rel_path}' for preview: {e}"
            print(error_msg, file=sys.stderr)
            errors_encountered.append(error_msg)

    full_preview = "\n".join(preview_content_parts).strip()

    return jsonify({
        "preview_content": full_preview,
        "errors": errors_encountered
    })


# (process route remains mostly the same, ensure it uses BASE_DIR correctly)
@app.route('/process', methods=['POST'])
def process_files():
    """Handles the FINAL form submission for concatenation."""
    selected_files_rel_paths = request.form.getlist('selected_files')
    prompt = request.form.get('prompt', '').strip()
    current_view_path = request.form.get('current_path', '')

    if not selected_files_rel_paths:
        flash("No files were selected.", 'warning')
        return redirect(url_for('browse', path=current_view_path))

    concatenated_content_parts = []
    errors_encountered = []

    # 1. Add the prompt first if it exists
    if prompt:
        concatenated_content_parts.append("--- User Prompt ---")
        concatenated_content_parts.append(prompt)
        concatenated_content_parts.append("--- End User Prompt ---")
        concatenated_content_parts.append("\n")

    # 2. Add content from selected files
    for rel_path in selected_files_rel_paths:
        abs_path = os.path.join(BASE_DIR, rel_path.strip('/')) # Use BASE_DIR

        if not is_safe_path(abs_path) or not os.path.isfile(abs_path):
            error_msg = f"Security Denied or Invalid File: '{rel_path}'"
            print(f"Warning: {error_msg}", file=sys.stderr)
            errors_encountered.append(error_msg)
            continue

        try:
            concatenated_content_parts.append(f"--- Content from: {rel_path} ---") # Final Header
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                concatenated_content_parts.append(content)
            concatenated_content_parts.append("--- End Content ---")
            concatenated_content_parts.append("\n")
        except Exception as e:
            error_msg = f"Error reading file '{rel_path}': {e}"
            print(error_msg, file=sys.stderr)
            errors_encountered.append(error_msg)

    # 3. Add errors
    if errors_encountered:
        concatenated_content_parts.append("\n--- Errors Encountered During Processing ---")
        concatenated_content_parts.extend(errors_encountered)

    final_output = "\n".join(concatenated_content_parts).strip()

    # --- Re-render the browser view ---
    directories, files, list_error = get_directory_contents(current_view_path)
    if list_error:
        flash(f"Note: Error reloading directory view '{current_view_path}': {list_error}", 'warning')

    parent_path = None
    if current_view_path:
        parent_dir = os.path.dirname(current_view_path)
        parent_path = parent_dir if parent_dir else ""
        parent_path = parent_path.replace(os.sep, '/')

    return render_template(
        'browser.html',
        current_relative_path=current_view_path.replace(os.sep, '/'),
        parent_path=parent_path,
        directories=directories or [],
        files=files or [],
        output=final_output # Pass final combined output
    )


# --- Entry Point for `pipx run` / `file-prompter` command ---
# (run_server function remains the same)
def run_server():
    """Function called by the console script entry point."""
    print(f"--- File Prompter ---")
    print(f"--- Serving files from: {BASE_DIR}")
    # Use static_folder path derived earlier
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


# --- Allow direct execution for development ---
# (if __name__ == '__main__': block remains the same)
if __name__ == '__main__':
    print("[DEVELOPMENT MODE]")
    print(f"Base Directory (CWD): {BASE_DIR}")
    print(f"Template Folder: {template_folder}")
    print(f"Static Folder: {static_folder}") # Print static folder path
    print("Run `python src/file_prompter/app.py` from your project root.")
    print("Access: http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)