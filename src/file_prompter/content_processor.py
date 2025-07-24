import os
import sys
try:
    from .file_utils import is_safe_path
except ImportError:
    from file_utils import is_safe_path

def generate_preview_content(selected_files_rel_paths, base_dir):
    """Generate preview content for selected files."""
    preview_content_parts = []
    errors_encountered = []
    
    for rel_path in selected_files_rel_paths:
        abs_path = os.path.join(base_dir, rel_path.strip('/'))
        if not is_safe_path(abs_path, base_dir) or not os.path.isfile(abs_path):
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
    return full_preview, errors_encountered

def generate_final_content(selected_files_rel_paths, prompt, base_dir):
    """Generate final concatenated content with prompt and selected files."""
    concatenated_content_parts = []
    errors_encountered = []

    if prompt:
        concatenated_content_parts.append("--- User Prompt ---")
        concatenated_content_parts.append(prompt)
        concatenated_content_parts.append("--- End User Prompt ---")
        concatenated_content_parts.append("\n")

    if not selected_files_rel_paths and not prompt:
        return "", ["No files selected and no prompt provided."]

    for rel_path in selected_files_rel_paths:
        abs_path = os.path.join(base_dir, rel_path.strip('/'))

        if not is_safe_path(abs_path, base_dir) or not os.path.isfile(abs_path):
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
    return final_output, errors_encountered 