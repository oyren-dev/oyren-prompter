FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY src/file_prompter/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ .

# Expose the port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV WORKSPACE_DIR=/workspace
ENV FLASK_PORT=5000

# Create a volume mount point for the user's directory
VOLUME ["/workspace"]

# Change working directory to workspace by default
WORKDIR /workspace

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${FLASK_PORT}/ || exit 1

# Run the application using the run_server function
CMD ["python", "-c", "import sys; sys.path.insert(0, '/app'); from file_prompter.app import run_server; run_server()"] 