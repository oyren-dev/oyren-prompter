# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Oyren Prompter is a Flask-based web application that allows users to browse and select multiple files from their local filesystem, combine their contents, and prepend a custom prompt. It's designed as a companion utility for AI development tools, particularly oyren.dev, to help construct prompts from codebases.

## Core Architecture

The application follows a modular Flask architecture with clear separation of concerns:

- `src/file_prompter/app.py` - Main Flask application entry point and server configuration
- `src/file_prompter/routes.py` - All HTTP route handlers and request processing
- `src/file_prompter/file_utils.py` - File system operations and security utilities
- `src/file_prompter/content_processor.py` - Content generation and file concatenation logic
- `src/file_prompter/templates/browser.html` - Single-page web interface
- `src/file_prompter/static/` - Static assets (logo, etc.)

## Development Commands

### NPX Usage (Recommended)
```bash
# Run directly with npx (auto-installs and launches)
npx oyren-prompter

# With custom port and directory
npx oyren-prompter --port 3000 --directory /path/to/project

# Enable debug mode
npx oyren-prompter --debug
```

### Local Development
```bash
# Run in development mode (port 5001, debug enabled)
python src/file_prompter/app.py

# Install as package and run (production mode, port 5000)
pip install -e .
file-prompter
```

### Docker Development
```bash
# Build and run with Docker
docker build -t oyren-prompter .
docker run -p 5000:5000 -v "$(pwd):/workspace" oyren-prompter

# Or use Docker Compose
docker-compose up
```

## Key Security Features

The application implements several security measures in `file_utils.py`:
- Path traversal protection via `is_safe_path()` function
- All file access is restricted to the configured base directory
- Input validation for all file paths and user data

## Configuration

- `BASE_DIR` environment variable controls the root directory (defaults to current working directory)
- `WORKSPACE_DIR` environment variable used in Docker deployments
- Flask secret key is auto-generated using `os.urandom(24)`

## New Features (Latest Version)

### Bulk File Selection
- **Select by Extension**: Choose all files with specific extensions (`.py`, `.js`, etc.)
- **Select All Visible**: Select all files currently displayed in the browser
- **Select Current Directory**: Select all files in current directory (with recursive option)
- **Smart Filtering**: Dynamic extension dropdown populated from available files

### File Content Search
- **Full-text Search**: Search within file contents across your entire project
- **Regex Support**: Use regular expressions for advanced pattern matching
- **Extension Filtering**: Limit search to specific file types
- **Case Sensitivity**: Toggle case-sensitive search
- **Live Results**: Interactive search results with file and line number links

### Keyboard Shortcuts
- **Shift + Space**: Open file content search modal
- **Ctrl/Cmd + A**: Select all visible files (when not in input fields)
- **Escape**: Close modals or clear search
- **Enter**: Perform search when in search input

## API Endpoints

### Core Endpoints
- `GET /` and `/browse/<path:path>` - File browser interface
- `POST /preview_content` - JSON API for file content preview
- `POST /process` - JSON API for final content generation with prompt

### New API Endpoints
- `POST /api/files_by_extension` - Get files by extension(s) with recursive option
- `POST /api/search_content` - Search file contents with regex and filtering
- `GET /api/available_extensions` - Get all available file extensions in directory

## NPX Integration

The application is now available as an npm package with Node.js wrapper:
- `package.json` defines npm package configuration
- `launcher.js` Node.js script that launches Python Flask app
- Uses `python-shell` for cross-platform Python execution
- Supports command-line options for port, directory, and debug mode

## Package Structure

The project uses modern Python packaging with `pyproject.toml`:
- Entry point: `file-prompter` command maps to `file_prompter.app:run_server`
- Package discovery in `src/` directory
- Includes templates and static files in package data
- NPX support via Node.js wrapper in project root