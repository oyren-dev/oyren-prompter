import os
import re
from flask import render_template, request, flash, jsonify
try:
    from .file_utils import get_directory_contents, get_all_files_in_directory, get_files_by_extension, search_file_contents
    from .content_processor import generate_preview_content, generate_final_content
except ImportError:
    from file_utils import get_directory_contents, get_all_files_in_directory, get_files_by_extension, search_file_contents
    from content_processor import generate_preview_content, generate_final_content

def setup_routes(app, base_dir):
    """Set up Flask routes for the application."""
    
    @app.route('/')
    @app.route('/browse/')
    @app.route('/browse/<path:path>')
    def browse(path=""):
        relative_path = path.strip('/')
        directories, files, error = get_directory_contents(relative_path, base_dir)
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

    @app.route('/preview_content', methods=['POST'])
    def preview_content():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        selected_files_rel_paths = data.get('selected_files', [])
        if not isinstance(selected_files_rel_paths, list):
            return jsonify({"error": "Invalid data format"}), 400
        
        preview_content, errors_encountered = generate_preview_content(selected_files_rel_paths, base_dir)
        
        return jsonify({
            "preview_content": preview_content,
            "errors": errors_encountered
        })

    @app.route('/process', methods=['POST'])
    def process_files():
        """Handles AJAX request to generate final output and returns JSON."""
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        selected_files_rel_paths = data.get('selected_files', [])
        selected_directories = data.get('selected_directories', [])
        prompt = data.get('prompt', '').strip()

        if not isinstance(selected_files_rel_paths, list):
            return jsonify({"error": "Invalid selected_files format"}), 400
        if not isinstance(selected_directories, list):
            return jsonify({"error": "Invalid selected_directories format"}), 400
        if not isinstance(prompt, str):
            return jsonify({"error": "Invalid prompt format"}), 400

        # Add all files from selected directories
        all_files = selected_files_rel_paths.copy()
        for directory in selected_directories:
            directory_files = get_all_files_in_directory(directory, base_dir)
            all_files.extend(directory_files)

        # Remove duplicates while preserving order
        seen = set()
        unique_files = []
        for file in all_files:
            if file not in seen:
                seen.add(file)
                unique_files.append(file)

        final_output, errors_encountered = generate_final_content(unique_files, prompt, base_dir)

        return jsonify({
            "final_output": final_output,
            "errors": errors_encountered
        })

    @app.route('/api/files_by_extension', methods=['POST'])
    def files_by_extension():
        """Get all files with specified extensions in current directory."""
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        extensions = data.get('extensions', [])
        current_path = data.get('current_path', '')
        recursive = data.get('recursive', False)
        
        if not isinstance(extensions, list):
            return jsonify({"error": "Extensions must be a list"}), 400
        
        try:
            files = get_files_by_extension(extensions, current_path, base_dir, recursive)
            return jsonify({"files": files})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/search_content', methods=['POST'])
    def search_content():
        """Search for text within file contents."""
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        query = data.get('query', '').strip()
        current_path = data.get('current_path', '')
        file_extensions = data.get('file_extensions', [])
        case_sensitive = data.get('case_sensitive', False)
        use_regex = data.get('use_regex', False)
        max_results = data.get('max_results', 50)
        
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        try:
            results = search_file_contents(
                query, current_path, base_dir, 
                file_extensions, case_sensitive, use_regex, max_results
            )
            return jsonify({"results": results})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/available_extensions', methods=['GET'])
    def available_extensions():
        """Get all file extensions available in the current directory."""
        current_path = request.args.get('path', '')
        
        try:
            directories, files, error = get_directory_contents(current_path, base_dir)
            if error:
                return jsonify({"error": error}), 400
            
            extensions = set()
            for file_item in files:
                file_name = file_item['name']
                if '.' in file_name:
                    ext = '.' + file_name.split('.')[-1].lower()
                    extensions.add(ext)
            
            # Get extensions from subdirectories if requested
            recursive = request.args.get('recursive', 'false').lower() == 'true'
            if recursive:
                for dir_item in directories:
                    try:
                        sub_files = get_all_files_in_directory(dir_item['rel_path'], base_dir)
                        for file_path in sub_files:
                            file_name = os.path.basename(file_path)
                            if '.' in file_name:
                                ext = '.' + file_name.split('.')[-1].lower()
                                extensions.add(ext)
                    except:
                        continue
            
            return jsonify({"extensions": sorted(list(extensions))})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 