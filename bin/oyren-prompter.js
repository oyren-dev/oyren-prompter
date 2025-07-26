#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
let port = 37465;

// Check for port argument
for (let i = 0; i < args.length; i++) {
    if (args[i] === '-p' || args[i] === '--port') {
        if (i + 1 < args.length) {
            const customPort = parseInt(args[i + 1]);
            if (!isNaN(customPort) && customPort > 0 && customPort < 65536) {
                port = customPort;
            } else {
                console.error('Error: Invalid port number. Must be between 1 and 65535.');
                process.exit(1);
            }
        }
    } else if (args[i] === '-h' || args[i] === '--help') {
        console.log(`
Oyren Prompter - Browse and combine file contents for AI prompts

Usage: npx oyren-prompter [options]

Options:
  -p, --port <port>  Specify custom port (default: 37465)
  -h, --help         Show this help message

Examples:
  npx oyren-prompter                 # Start on default port 37465
  npx oyren-prompter -p 8080         # Start on port 8080
`);
        process.exit(0);
    }
}

// Check if Docker is installed
const checkDocker = spawn('docker', ['--version']);

checkDocker.on('error', (err) => {
    console.error(`
❌ Docker is not installed or not available in PATH.

To use Oyren Prompter, you need to install Docker:

1. Visit https://www.docker.com/get-started
2. Download Docker Desktop for your operating system
3. Install and start Docker
4. Try running this command again

Alternative: Use the Python version with pipx:
  pipx run --spec git+https://github.com/oyren-dev/oyren-prompter.git oyren-prompter
`);
    process.exit(1);
});

checkDocker.on('close', (code) => {
    if (code !== 0) {
        console.error('Error: Failed to verify Docker installation.');
        process.exit(1);
    }

    // Docker is installed, run the container
    console.log(`Starting Oyren Prompter on port ${port}...`);
    console.log(`Access the application at: http://localhost:${port}`);
    console.log('Press Ctrl+C to stop the server.\n');

    const dockerRun = spawn('docker', [
        'run',
        '--rm',
        '-it',
        '-v', `${process.cwd()}:/project`,
        '-p', `${port}:37465`,
        'oyrendev/prompter:latest'
    ], {
        stdio: 'inherit'
    });

    dockerRun.on('error', (err) => {
        console.error('Error running Docker container:', err.message);
        process.exit(1);
    });

    dockerRun.on('close', (code) => {
        if (code !== 0 && code !== 130) { // 130 is Ctrl+C
            console.error(`Docker container exited with code ${code}`);
            
            // If it's likely a "image not found" error
            if (code === 125) {
                console.log(`
It looks like the Docker image is not available locally.
Docker will automatically pull the image. Please wait...

If the problem persists, try pulling manually:
  docker pull oyrendev/prompter:latest
`);
            }
        }
    });

    // Handle Ctrl+C gracefully
    process.on('SIGINT', () => {
        console.log('\nShutting down Oyren Prompter...');
        dockerRun.kill('SIGINT');
    });
});