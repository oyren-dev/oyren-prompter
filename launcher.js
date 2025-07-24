#!/usr/bin/env node

const { PythonShell } = require('python-shell');
const { program } = require('commander');
const chalk = require('chalk');
const path = require('path');
const fs = require('fs');

program
  .name('oyren-prompter')
  .description('A local web tool for browsing files and preparing AI prompts')
  .version('1.0.0')
  .option('-p, --port <port>', 'port to run the server on', '5000')
  .option('-d, --directory <directory>', 'base directory to serve files from', process.cwd())
  .option('--debug', 'enable debug mode')
  .parse();

const options = program.opts();

console.log(chalk.blue.bold('🚀 Starting Oyren Prompter...'));
console.log(chalk.gray(`📁 Serving files from: ${options.directory}`));
console.log(chalk.gray(`🌐 Port: ${options.port}`));

// Check if Python is available
function checkPython() {
  return new Promise((resolve, reject) => {
    PythonShell.getVersion()
      .then(version => {
        console.log(chalk.green(`✅ Python ${version} found`));
        resolve(version);
      })
      .catch(err => {
        console.error(chalk.red('❌ Python not found. Please install Python 3.7+ and try again.'));
        console.error(chalk.gray('   Download from: https://www.python.org/downloads/'));
        reject(err);
      });
  });
}

// Install Python dependencies
function installDependencies() {
  return new Promise((resolve, reject) => {
    console.log(chalk.yellow('📦 Installing Python dependencies...'));
    
    const requirementsPath = path.join(__dirname, 'src', 'file_prompter', 'requirements.txt');
    
    if (!fs.existsSync(requirementsPath)) {
      console.log(chalk.green('✅ No additional Python dependencies needed'));
      resolve();
      return;
    }

    const installOptions = {
      mode: 'text',
      args: ['-m', 'pip', 'install', '-r', requirementsPath],
      scriptPath: '',
      pythonOptions: ['-u']
    };

    PythonShell.run('python', installOptions)
      .then(() => {
        console.log(chalk.green('✅ Python dependencies installed successfully'));
        resolve();
      })
      .catch(err => {
        console.warn(chalk.yellow('⚠️  Failed to install dependencies automatically'));
        console.warn(chalk.gray('   You may need to run: pip install Flask'));
        // Don't reject, try to continue anyway
        resolve();
      });
  });
}

// Start the Flask application
function startFlaskApp() {
  return new Promise((resolve, reject) => {
    console.log(chalk.blue('🔥 Starting Flask server...'));
    
    const scriptPath = path.join(__dirname, 'src', 'file_prompter');
    
    const pythonOptions = {
      mode: 'text',
      pythonPath: 'python',
      scriptPath: scriptPath,
      env: {
        ...process.env,
        WORKSPACE_DIR: options.directory,
        FLASK_PORT: options.port,
        FLASK_DEBUG: options.debug ? '1' : '0'
      }
    };

    // Launch the Flask app
    const pyshell = new PythonShell('app.py', pythonOptions);
    
    pyshell.on('message', function (message) {
      console.log(message);
      
      // Look for server start message
      if (message.includes('Access in browser')) {
        console.log(chalk.green.bold('✅ Server started successfully!'));
        console.log(chalk.cyan(`🌐 Open your browser and go to: http://localhost:${options.port}`));
        console.log(chalk.gray('   Press Ctrl+C to stop the server'));
      }
    });

    pyshell.on('stderr', function (stderr) {
      if (options.debug) {
        console.error(chalk.red(stderr));
      }
    });

    pyshell.on('error', function (err) {
      console.error(chalk.red('❌ Failed to start Flask server:'));
      console.error(chalk.red(err.message));
      reject(err);
    });

    pyshell.on('close', function () {
      console.log(chalk.yellow('👋 Oyren Prompter stopped'));
      process.exit(0);
    });

    // Handle process termination
    process.on('SIGINT', () => {
      console.log(chalk.yellow('\n🛑 Shutting down Oyren Prompter...'));
      pyshell.kill();
    });

    process.on('SIGTERM', () => {
      console.log(chalk.yellow('\n🛑 Shutting down Oyren Prompter...'));
      pyshell.kill();
    });
  });
}

// Main execution
async function main() {
  try {
    await checkPython();
    await installDependencies();
    await startFlaskApp();
  } catch (error) {
    console.error(chalk.red('❌ Failed to start Oyren Prompter:'), error.message);
    process.exit(1);
  }
}

main();