## Support This Project

If you find Oyren Prompter useful, consider supporting its development!

<a href="https://buymeacoffee.com/vorashil" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 174px !important;" >
</a>

Or, use the direct link: [https://buymeacoffee.com/vorashil](https://buymeacoffee.com/vorashil)

---

# Oyren Prompter

A simple, local web-based tool to browse files and directories, select multiple files, concatenate their content, and prepend a custom prompt. Ideal for quickly gathering context from codebases or text files to use with AI chat models (like ChatGPT, Claude, Gemini, etc.).

The tool runs a local web server, and you interact with it through your browser, ensuring your files stay on your machine. Powered by [Oyren.dev](https://oyren.dev).

## Quick Start

**Prerequisites:** Python 3.7+, Git, and `pipx` (see one-time setup below).

1.  `cd` into the directory you want to work with:
    ```bash
    cd /path/to/your/project/or/files
    ```
2.  Run the prompter directly from GitHub using `pipx`:
    ```bash
    pipx run --spec git+https://github.com/oyren-dev/oyren-prompter.git oyren-prompter
    ```
3.  Open your browser to `http://127.0.0.1:5000`.
4.  Press `CTRL+C` in the terminal to stop.

## Prerequisites (One-Time Setup)

Before running Oyren Prompter using the recommended `pipx` method, ensure you have:

1.  **Python:** Version 3.7 or higher.
    *   **macOS/Linux:** Check with `python3 --version`. Install from [python.org](https://www.python.org/) if needed.
    *   **Windows:** Check with `python --version` or `py --version`. Install from [python.org](https://www.python.org/) or the Microsoft Store. **Ensure Python is added to your PATH during installation.**
2.  **Git:** Required to fetch code from GitHub.
    *   **macOS:** Often pre-installed or installable via `xcode-select --install` or `brew install git`.
    *   **Windows/Linux:** Download from [git-scm.com](https://git-scm.com/).
3.  **pipx:** The tool used to run Python applications in isolated environments. Install it **once** based on your OS:

    *   **macOS (Recommended):**
        *   Install Homebrew if you don't have it: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
        *   Install `pipx` using Homebrew:
            ```bash
            brew install pipx
            pipx ensurepath
            ```
        *   **Restart your terminal** after running `ensurepath`.

    *   **Windows:**
        *   Install `pipx` using Python's pip (ensure Python is in your PATH):
            ```bash
            # You might need to use 'py -m pip' instead of 'python -m pip'
            python -m pip install --user pipx
            python -m pipx ensurepath
            ```
        *   **Restart your Command Prompt or PowerShell** after running `ensurepath`.

    *   **Linux (Debian/Ubuntu/Mint):**
        ```bash
        sudo apt update
        sudo apt install pipx
        pipx ensurepath
        ```
        *   **Restart your terminal** after running `ensurepath`. *(Alternatively, use `python3 -m pip install --user pipx` followed by `python3 -m pipx ensurepath` if the package isn't available or up-to-date).*

    *   **Linux (Fedora/CentOS/RHEL):**
        ```bash
        sudo dnf install pipx
        pipx ensurepath
        ```
        *   **Restart your terminal** after running `ensurepath`. *(Alternatively, use `python3 -m pip install --user pipx` followed by `python3 -m pipx ensurepath`)*.

    *   **Verify pipx:** After restarting your terminal, run `pipx --version`. You should see a version number.

## Running Oyren Prompter (Recommended Method: pipx)

Once the prerequisites (Python, Git, pipx) are set up, you can run Oyren Prompter from any directory:

1.  **Navigate to Target Directory:** Open your terminal and change (`cd`) to the folder containing the files you want to work with.
    ```bash
    cd /path/to/your/project/or/files
    ```
2.  **Run:** Use `pipx` to execute the latest version directly from GitHub:
    ```bash
    pipx run --spec git+https://github.com/oyren-dev/oyren-prompter.git oyren-prompter
    ```
    *   This downloads the code temporarily, sets up its environment, and runs it without permanently installing it.*
3.  **Access:** Open your web browser to `http://127.0.0.1:5000`.
4.  **Stop:** Press `CTRL+C` in the terminal where `pipx run` is active.

## Optional: macOS Installation via Homebrew

If you are on macOS and prefer to install Oyren Prompter persistently using Homebrew (instead of using `pipx run` each time):

1.  **Add the Oyren Tap (if you haven't already):**
    ```bash
    brew tap oyren-dev/homebrew-oyren
    ```
2.  **Install Oyren Prompter:**
    ```bash
    brew install oyren-prompter
    ```
3.  **Run:**
    *   `cd /path/to/your/project/or/files`
    *   `oyren-prompter`
4.  **Update:**
    ```bash
    brew upgrade oyren-prompter
    ```

## Usage

(Instructions for using the web interface remain the same - browse, select, preview, prompt, generate, copy, paste)

1.  **Browse:** Click directory names (`📁`) to navigate. Click `⬆️ .. [Up]` to go back.
2.  **Select:** Check boxes next to files (`📄`). The "Selected Files" list updates instantly.
3.  **Preview (Optional):** Click "Show/Hide Content Preview" to view/hide combined content of selected files.
4.  **Prompt:** Enter your instructions in the "Your Prompt" box.
5.  **Generate:** Click "Generate Final Output".
6.  **Copy:** Select and copy the text from the "Final Output (Copy Below)" area.
7.  **Paste:** Paste into your AI chat interface.

## Contributing

Found a bug or have an idea? Please open an issue on the GitHub repository:
[https://github.com/oyren-dev/oyren-prompter/issues](https://github.com/oyren-dev/oyren-prompter/issues)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/oyren-dev/oyren-prompter/blob/main/LICENSE) file for details.