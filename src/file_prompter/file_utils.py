import os
import sys
import re
import glob

def is_safe_path(path_to_check, base_dir):
    """Check if a path is safe to access within the base directory."""
    try:
        abs_path = os.path.abspath(path_to_check)
        return os.path.commonpath([base_dir, abs_path]) == base_dir
    except ValueError:
        return False

def get_directory_contents(relative_path="", base_dir=None):
    """Get the contents of a directory safely."""
    if base_dir is None:
        base_dir = os.path.abspath(os.getcwd())
    
    clean_relative_path = relative_path.strip('/')
    current_abs_path = os.path.join(base_dir, clean_relative_path)
    
    if not is_safe_path(current_abs_path, base_dir):
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
        item_rel_path = os.path.relpath(item_abs_path, base_dir)
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

def get_all_files_in_directory(directory_path, base_dir):
    """Recursively get all files in a directory."""
    files = []
    abs_directory_path = os.path.join(base_dir, directory_path.strip('/'))
    
    if not is_safe_path(abs_directory_path, base_dir) or not os.path.isdir(abs_directory_path):
        return files
    
    try:
        for root, dirs, file_names in os.walk(abs_directory_path):
            for file_name in file_names:
                file_abs_path = os.path.join(root, file_name)
                file_rel_path = os.path.relpath(file_abs_path, base_dir)
                file_rel_path_norm = file_rel_path.replace(os.sep, '/')
                files.append(file_rel_path_norm)
    except OSError as e:
        print(f"Warning: Error walking directory '{directory_path}': {e}", file=sys.stderr)
    
    return files

def get_files_by_extension(extensions, current_path="", base_dir=None, recursive=False):
    """Get all files with specified extensions."""
    if base_dir is None:
        base_dir = os.path.abspath(os.getcwd())
    
    files = []
    clean_current_path = current_path.strip('/')
    search_path = os.path.join(base_dir, clean_current_path)
    
    if not is_safe_path(search_path, base_dir) or not os.path.isdir(search_path):
        return files
    
    # Normalize extensions (ensure they start with .)
    normalized_extensions = []
    if extensions:  # Only normalize if extensions list is not empty
        for ext in extensions:
            if ext and not ext.startswith('.'):
                ext = '.' + ext
            normalized_extensions.append(ext.lower())
    
    try:
        if recursive:
            # Use os.walk for recursive search
            for root, dirs, file_names in os.walk(search_path):
                for file_name in file_names:
                    file_ext = os.path.splitext(file_name)[1].lower()
                    # If no extensions specified, include all files; otherwise filter by extension
                    if not normalized_extensions or file_ext in normalized_extensions:
                        file_abs_path = os.path.join(root, file_name)
                        file_rel_path = os.path.relpath(file_abs_path, base_dir)
                        file_rel_path_norm = file_rel_path.replace(os.sep, '/')
                        files.append(file_rel_path_norm)
        else:
            # Search only in current directory
            for file_name in os.listdir(search_path):
                file_abs_path = os.path.join(search_path, file_name)
                if os.path.isfile(file_abs_path):
                    file_ext = os.path.splitext(file_name)[1].lower()
                    # If no extensions specified, include all files; otherwise filter by extension
                    if not normalized_extensions or file_ext in normalized_extensions:
                        file_rel_path = os.path.relpath(file_abs_path, base_dir)
                        file_rel_path_norm = file_rel_path.replace(os.sep, '/')
                        files.append(file_rel_path_norm)
    except OSError as e:
        print(f"Warning: Error getting files by extension: {e}", file=sys.stderr)
    
    return sorted(files)

def search_file_contents(query, current_path="", base_dir=None, file_extensions=None, 
                        case_sensitive=False, use_regex=False, max_results=50):
    """Search for text within file contents."""
    if base_dir is None:
        base_dir = os.path.abspath(os.getcwd())
    
    results = []
    clean_current_path = current_path.strip('/')
    search_path = os.path.join(base_dir, clean_current_path)
    
    if not is_safe_path(search_path, base_dir) or not os.path.isdir(search_path):
        return results
    
    # Prepare search pattern
    if use_regex:
        try:
            pattern = re.compile(query, re.IGNORECASE if not case_sensitive else 0)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    else:
        pattern = query if case_sensitive else query.lower()
    
    # Normalize file extensions
    target_extensions = None
    if file_extensions:
        target_extensions = set()
        for ext in file_extensions:
            if ext and not ext.startswith('.'):
                ext = '.' + ext
            target_extensions.add(ext.lower())
    
    try:
        # Search through files recursively
        for root, dirs, file_names in os.walk(search_path):
            for file_name in file_names:
                if len(results) >= max_results:
                    break
                
                file_abs_path = os.path.join(root, file_name)
                file_rel_path = os.path.relpath(file_abs_path, base_dir)
                file_rel_path_norm = file_rel_path.replace(os.sep, '/')
                
                # Check file extension filter
                if target_extensions:
                    file_ext = os.path.splitext(file_name)[1].lower()
                    if file_ext not in target_extensions:
                        continue
                
                # Skip binary files (basic check)
                if is_likely_binary_file(file_abs_path):
                    continue
                
                try:
                    with open(file_abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        matches = []
                        if use_regex:
                            for match in pattern.finditer(content):
                                line_num = content[:match.start()].count('\n') + 1
                                line_start = content.rfind('\n', 0, match.start()) + 1
                                line_end = content.find('\n', match.end())
                                if line_end == -1:
                                    line_end = len(content)
                                line_content = content[line_start:line_end]
                                
                                matches.append({
                                    "line": line_num,
                                    "content": line_content.strip(),
                                    "match": match.group()
                                })
                        else:
                            search_content = content if case_sensitive else content.lower()
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                search_line = line if case_sensitive else line.lower()
                                if pattern in search_line:
                                    matches.append({
                                        "line": i + 1,
                                        "content": line.strip(),
                                        "match": query
                                    })
                        
                        if matches:
                            results.append({
                                "file": file_rel_path_norm,
                                "matches": matches[:10]  # Limit matches per file
                            })
                
                except (OSError, UnicodeDecodeError):
                    # Skip files that can't be read
                    continue
            
            if len(results) >= max_results:
                break
                
    except OSError as e:
        print(f"Warning: Error searching file contents: {e}", file=sys.stderr)
    
    return results

def is_likely_binary_file(file_path):
    """Check if a file is likely binary by examining its first few bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # Null bytes indicate binary
                return True
            # Check for high ratio of non-printable characters
            printable_chars = sum(1 for c in chunk if c >= 32 and c <= 126 or c in [9, 10, 13])
            if len(chunk) > 0 and printable_chars / len(chunk) < 0.7:
                return True
    except (OSError, IOError):
        return True
    return False 