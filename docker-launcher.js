#!/usr/bin/env node

const { spawn } = require('child_process');
const { program } = require('commander');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

program
  .name('oyren-prompter')
  .description('A local web tool for browsing files and preparing AI prompts')
  .version('1.0.0')
  .option('-p, --port <port>', 'port to run the server on', '3020')
  .option('-d, --directory <directory>', 'base directory to serve files from', process.cwd())
  .option('--build', 'force rebuild the Docker image')
  .parse();

const options = program.opts();

console.log(chalk.blue.bold('🚀 Starting Oyren Prompter with Docker...'));
console.log(chalk.gray(`📁 Serving files from: ${options.directory}`));
console.log(chalk.gray(`🌐 Port: ${options.port}`));

// Check if Docker is available
function checkDocker() {
  return new Promise((resolve, reject) => {
    const dockerCheck = spawn('docker', ['--version'], { stdio: 'pipe' });
    
    dockerCheck.on('close', (code) => {
      if (code === 0) {
        console.log(chalk.green('✅ Docker found'));
        resolve();
      } else {
        console.error(chalk.red('❌ Docker not found. Please install Docker and try again.'));
        console.error(chalk.gray('   Download from: https://www.docker.com/products/docker-desktop'));
        reject(new Error('Docker not available'));
      }
    });
    
    dockerCheck.on('error', () => {
      console.error(chalk.red('❌ Docker not found. Please install Docker and try again.'));
      reject(new Error('Docker not available'));
    });
  });
}

// Build Docker image
function buildImage() {
  return new Promise((resolve, reject) => {
    console.log(chalk.yellow('🔨 Building Docker image...'));
    
    const build = spawn('docker', ['build', '-t', 'oyren-prompter', '.'], {
      stdio: 'inherit',
      cwd: __dirname
    });
    
    build.on('close', (code) => {
      if (code === 0) {
        console.log(chalk.green('✅ Docker image built successfully'));
        resolve();
      } else {
        console.error(chalk.red('❌ Failed to build Docker image'));
        reject(new Error('Docker build failed'));
      }
    });
  });
}

// Check if image exists
function imageExists() {
  return new Promise((resolve) => {
    const check = spawn('docker', ['images', '-q', 'oyren-prompter'], { stdio: 'pipe' });
    let output = '';
    
    check.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    check.on('close', () => {
      resolve(output.trim().length > 0);
    });
  });
}

// Run Docker container
function runContainer() {
  return new Promise((resolve, reject) => {
    console.log(chalk.blue('🐳 Starting Docker container...'));
    
    // Stop any existing container
    spawn('docker', ['stop', 'oyren-prompter-instance'], { stdio: 'pipe' });
    spawn('docker', ['rm', 'oyren-prompter-instance'], { stdio: 'pipe' });
    
    // Start new container
    const run = spawn('docker', [
      'run',
      '--name', 'oyren-prompter-instance',
      '--rm',
      '-p', `${options.port}:5000`,
      '-v', `${path.resolve(options.directory)}:/workspace`,
      '-e', `FLASK_PORT=5000`,
      'oyren-prompter'
    ], {
      stdio: 'inherit'
    });
    
    // Give the container a moment to start
    setTimeout(() => {
      console.log(chalk.green.bold('✅ Oyren Prompter is starting up!'));
      console.log(chalk.cyan(`🌐 Open your browser and go to: http://localhost:${options.port}`));
      console.log(chalk.gray('   Press Ctrl+C to stop the server'));
    }, 3000);
    
    run.on('close', (code) => {
      if (code === 0) {
        console.log(chalk.yellow('👋 Oyren Prompter stopped'));
      } else {
        console.error(chalk.red('❌ Container exited with error'));
      }
      process.exit(code);
    });
    
    // Handle process termination
    process.on('SIGINT', () => {
      console.log(chalk.yellow('\n🛑 Shutting down Oyren Prompter...'));
      spawn('docker', ['stop', 'oyren-prompter-instance'], { stdio: 'inherit' });
    });
    
    process.on('SIGTERM', () => {
      console.log(chalk.yellow('\n🛑 Shutting down Oyren Prompter...'));
      spawn('docker', ['stop', 'oyren-prompter-instance'], { stdio: 'inherit' });
    });
  });
}

// Main execution
async function main() {
  try {
    await checkDocker();
    
    const exists = await imageExists();
    if (!exists || options.build) {
      await buildImage();
    } else {
      console.log(chalk.green('✅ Docker image found'));
    }
    
    await runContainer();
  } catch (error) {
    console.error(chalk.red('❌ Failed to start Oyren Prompter:'), error.message);
    process.exit(1);
  }
}

main();