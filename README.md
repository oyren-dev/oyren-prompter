# Oyren Prompter

**Oyren Prompter** is a local web tool that allows you to browse and select multiple files, combine their contents, and prepend a custom prompt. It’s perfect for preparing contextual input for AI chat models — while keeping your files 100% private and on your machine.

![Oyren Prompter Demo](./oyren-prompter-demo.mp4)

---

## 🌐 About [oyren.dev](https://oyren.dev)

> **oyren.dev** is a browser-based AI development platform that helps you build, test, and refine code faster using multiple AI models — no switching between tools, no file uploads. It’s designed for rapid prototyping and real-time code feedback, all in the browser.

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

- Python 3.7+
- Git
- `pipx` (recommended)
- Modern web browser

Install `pipx` using Homebrew (macOS):

``` 
brew install pipx
pipx ensurepath 
pipx --version
``` 

If `pipx` doesn't get installed properly, try restarting your terminal.

---

### 🛠 How to Run

You can launch Oyren Prompter with a single command:

``` 
pipx run --spec git+https://github.com/oyren-dev/oyren-prompter.git oyren-prompter
``` 

This will start a local Flask server that scans your files. You can then:

- Select the files you want to use
- Combine them into a single context
- Prepend a custom prompt
- Use the result with your favorite AI tool

✅ All files stay local — nothing is ever uploaded.

---

## 🤝 Contributing

We welcome contributions! Here’s how to get started:

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