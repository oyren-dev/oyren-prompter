FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY src/file_prompter/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ ./src/

# Set the working directory to the project root
WORKDIR /project

# Expose the port the app runs on
EXPOSE 37465

# Run the application
CMD ["python", "/app/src/file_prompter/app.py"]