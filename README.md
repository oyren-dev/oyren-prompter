# Oyren Prompter

**Oyren Prompter** is a local web tool that allows you to browse and select multiple files, combine their contents, and prepend a custom prompt. It's perfect for preparing contextual input for AI chat models — while keeping your files 100% private and on your machine.

✨ **New Features**: Modern dark mode UI, IDE-like experience, and streamlined AI integration!

![Oyren Prompter Demo](./oyren-prompter-demo.gif)

---

## 🌐 About [oyren.dev](https://oyren.dev)

> **oyren.dev** is a browser-based AI development platform that helps you build, test, and refine code faster using multiple AI models — no switching between tools, no file uploads. It's designed for rapid prototyping and real-time code feedback, all in the browser.

**Oyren Prompter** is a companion utility for oyren.dev to help users easily construct prompts from their codebase and use them with AI tools.

---

## Support This Project

If you find Oyren Prompter useful, consider supporting its development!

<a href="https://buymeacoffee.com/vorashil" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 174px !important;" >
</a>

Or, use the direct link: [https://buymeacoffee.com/vorashil](https://buymeacoffee.com/vorashil)

---

## 🚀 Getting Started

### Prerequisites

- **For Docker (Recommended):** Docker
- **For pipx:** Python 3.7+, Git, and `pipx`
- Modern web browser

---

## 🐳 Option 1: Run with Docker (Recommended)

The easiest way to run Oyren Prompter is using Docker. This method automatically handles all dependencies and setup.

### Quick Start

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run Oyren Prompter (pulls from Docker Hub automatically)
docker run -p 5000:5000 -v "$(pwd):/workspace" oyren/oyren-prompter
```

That's it! Open your browser and go to `http://localhost:5000`

### Alternative: Using Docker Compose

If you prefer Docker Compose, clone the repository first:

```bash
git clone https://github.com/oyren-dev/oyren-prompter.git
cd oyren-prompter
docker-compose up
```

### Build from source

If you want to build the Docker image yourself:

```bash
git clone https://github.com/oyren-dev/oyren-prompter.git
cd oyren-prompter
docker build -t oyren-prompter .
docker run -p 5000:5000 -v "$(pwd):/workspace" oyren-prompter
```

---

## 📦 Option 2: Run with pipx

You can also launch Oyren Prompter using pipx with a single command:

### Install pipx (if needed)

For macOS using Homebrew:
``` 
brew install pipx
pipx ensurepath 
pipx --version
``` 

If `pipx` doesn't get installed properly, try restarting your terminal.

### Run the application

``` 
pipx run --spec git+https://github.com/oyren-dev/oyren-prompter.git oyren-prompter
``` 

This will start a local Flask server that scans your files from the current directory.

---

## ✨ Features

- **🌓 Dark/Light Mode**: Modern IDE-like interface with toggle between themes
- **📁 File & Directory Selection**: Choose individual files or entire directories to include in your prompt
- **👁️ Live Preview**: See a preview of your selected content before generating the final output
- **💾 Smart Persistence**: Your prompts and selections are saved and persist when navigating between directories
- **🤖 ChatGPT Integration**: Direct integration with multiple ChatGPT models (GPT-4, GPT-4 Turbo, GPT-3.5)
- **🔌 Universal AI Support**: Easy copy-paste workflow for any AI service (Claude, Gemini, DeepSeek, etc.)
- **🔒 Safe & Private**: All files stay local — nothing is ever uploaded
- **🐳 Docker Ready**: Easy deployment with Docker Hub image

## 📋 How to Use

1. **🌐 Launch** the application using Docker or pipx
2. **🎨 Choose Theme** using the theme toggle in the header (dark/light mode)
3. **📂 Navigate** through your files using the file explorer
4. **✅ Select** the files and/or directories you want to include
5. **✍️ Add your prompt** in the text area (optional)
6. **👁️ Preview** your content to verify your selection
7. **📋 Generate & Copy** to get the combined content, or
8. **🚀 Send to ChatGPT** directly with your preferred model, or
9. **📄 Copy** and paste into any other AI service

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**  
   ```  git checkout -b your-feature-name ``` 
3. **Make your changes**
4. **Commit and push**  
   ```  git commit -m "Describe your change" ```   
   ```  git push origin your-feature-name ``` 
5. **Open a pull request** to the `main` branch

### Contribution Guidelines

- Write clear and concise commit messages
- Document any new features or config changes
- Feel free to open issues for bugs, questions, or suggestions

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).