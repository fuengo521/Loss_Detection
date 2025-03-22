# Getting Started

Welcome to our project! This guide will help you install the necessary tools, clone the repository, and set up everything so you can start contributing right away.

---

## Table of Contents
1. [Install VSCode](#VSCode)
2. [Install Git](#Git)
3. [Set Up GitHub & VSCode Integration](#SetUp)
4. [Clone the Repository](#Clone)
5. [Create & Activate a Virtual Environment](#Create)
6. [Run `startup.py`](#StartUp)
7. [Basic GitHub Workflow (Branching, Pull Requests, Syncing)](#Basic)
8. [Additional Resources](#Add)

---
<div id='VSCode'/>

## 1. Install VSCode

1. **Download VSCode** from [https://code.visualstudio.com/download](https://code.visualstudio.com/download).  
2. **Open VSCode**. This will be your main environment for writing code and managing version control.

> **Tip:** VSCode has an integrated terminal. You can open it via **View > Terminal** or using **Ctrl+Shift+~** (Windows) or **Cmd+Shift+~** (macOS).

---
<div id='Git'/>

## 2. Install Git

> Git is a version control system that lets you track changes and collaborate with others on the same codebase.

1. **Check if Git is already installed** by opening the VSCode terminal and typing:
   ```bash
   git --version
* If you see a version (e.g., git version 2.30.1), you’re all set.
* If not, follow these steps:

2. **Install Git:**
    * **Windows:** [Download Git for Windows](https://git-scm.com/downloads/win) and follow the installer prompts.
    * **macOS:** [Download Git for Mac](https://git-scm.com/download/mac) or install via Homebrew (`brew install git`)

<div id='SetUp'/>

## 3. Set Up GitHub & VSCode Integration

VSCode comes with built-in Git integration. To enhance GitHub support (like Pull Requests, Issues, etc.):

1. **Install the "GitHub Pull Requests" extension:**
    * In VSCode, got to **View > Extensions** (or press **Ctrl+Shift+X**).
    * Search for "**GitHub Pull Requests**" and install it.

2. **Sign in to GitHub** when prompted, so VSCode can link your account and repository.

If you want a quick tutorial on using Git in VSCode, check out:
* [Using Git & GitHub in VSCode (Intro)](https://youtu.be/z5jZ9lrSpqk?si=BeTU7jLE9cCjh0YQ)
* [Using Git & GitHub in VSCode (Branches, PRs & Merges)](https://youtu.be/Dedz4gRHezg?si=hj96eMzawNB-e4BO)

<div id='Clone'/>

## 4. Clone the Repository
Instead of manually typing commands, you can use VSCode's **Command Palette:**

1. **Open the Command Palette:**
    * **Windows:** `Ctrl + Shift + P`
    * **macOS:** `Cmd + Shift + P`
2. **Type "Git: Clone"** and select it.
3. **Enter the repository URL:**
    * You can find it on GitHub: **Go to your repo page > Code > HTTPS** (e.g., `https://github.com/YourUsername/RepoName.git`).
4. **Choose a folder** on your local machine where you want to close the project.
5. **Open the folder** once cloning completes.

>Alternatively, you can still use the terminal:
```bash
git clone https://github.com/YourUsername/RepoName.git
cd RepoName
code .
```
<div id='Create'/>

## 5. Create & Activate a Virtual Environment
A virtual environment ensures everyone uses the **same Python packages:**

1. **Open the VSCode Terminal:**
    * **View > Terminal** or **Ctrl+Shift+~** (Windows), **Cmd+Shift+~** (macOS)
2. **Navigate to the project root** if you aren't already there:
    ```bash
    cd path/to/RepoName
3. **Create a virtual environmnet** named `venv`:
    ```bash
    python -m venv venv
4. **Activate the environment:**
    * **Windows:**
    ```bash
    venv\Scripts\activate
    ```
    * **macOS:**
    ```bash
    source venv\bin\activate
    ```
You should see `(venv)` in your terminal prompt, indicating the environment is active.

<div id='StartUp'/>

## 6. Run `startup.py`
We have a **startup script** to install required libraries:

1. **With the virtual environmnet still active**, run:
```bash
python startup.py
```
2. This will:
    * Install all packages listed in `requirements.txt`
    * Print any helpful messages if somethng goes wrong.
> **Pro Tip:** If you see a warning that you are not in a virtual environment, simply activate the environment (see step 5) and re-run `startup.py`.

<div id='Basic'/>

## 7. Basic GitHub Workflow (Branching, Pull Requests, Synching)
### 7.1 Creating a Branch
When you want to add a new feature or fix a bug, create a new branch. You can do this in VSCode:

1. **Open the Source Control panel** (the Git icon in the sidebar).
2. **Click the Branch dropdown** and select "**Create new branch**".
3. Name your branch, e.g., `feature/new-data-cleaning`.
    * Use meaningful prefixes like:
        * **feature** - for a feature or enhancement
        * **bug** - for bug fixes
        * **hotfix** - for immediate or critical fixes
        * **chore** - for minor updates (like documentation or clean up)

### 7.2 Making Commit
After making changes:

1. **Open the Source Control panel** again.
2. You'll see your modified files listed.
3. **Stage your changes**: Click the plus icon (+) next to each file (or click the "Stage All Changes" button) to add them to the commit.
3. Write a **commit message** in the box (e.g., "Implement new data cleaning logic"), then click the checkmark to commit.

### 7.3 Pushing to GitHub

1. **Click the "Sync Changes"** or "Push" button in the Source Control panel.
2. The new branch will appear on GitHub.

### 7.4 Pull Requests & Merges

1. On GitHub, find your newly pushed branch
2. **Click "Compare & pull request"**.
3. Provide a description, then **open the Pull Request**.
4. Teammates can review and merge your changes into the `main` branch.

### 7.5 Keeping Up to Date
To sync your local code with the main repository:
* **VSCode:** Use the "Pull" button in Source Control, or
* **Terminal:**
    ```bash
    git checkout main
    git pull origin main
If your local code conflicts with changes on GitHub, Git will guide you through resolving merge conflicts.
> **Video:** For more on branches, PRs, merges, see [Using Git & GitHub in VSCode (Branches, PRs, & Merges)](https://youtu.be/Dedz4gRHezg?si=hj96eMzawNB-e4BO).

<div id='Add'/>

## 8. Additional Resources
* **Git**
    * [Official Git Docs](https://git-scm.com/doc)
* **VSCode**
    * [Intro to Git in VSCode Docs](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git)
* **YouTube Videos**
    * [Using Git & GitHub in VSCode (Intro)](https://youtu.be/z5jZ9lrSpqk?si=BeTU7jLE9cCjh0YQ)
    [Using Git & GitHub in VSCode (Branches, PRs & Merges)](https://youtu.be/Dedz4gRHezg?si=hj96eMzawNB-e4BO)

**That's it!** You should now be ready to start coding, analyzing data, and collaborating with the team.
Happy coding!