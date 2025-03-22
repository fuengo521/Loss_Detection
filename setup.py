import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "Craigslist_test.csv")

def get_venv_python():
    """Return the path to the virtual environment's python executable."""
    if sys.platform == "win32":
        return os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    else:
        return os.path.join(PROJECT_ROOT, "venv", "bin", "python")

def create_virtualenv():
    """Creates the virtual environment if it doesn't exist."""
    venv_path = os.path.join(PROJECT_ROOT, "venv")
    if not os.path.exists(venv_path):
        print("\n Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    print("\n Virtual environment created successfully!")
    print(" To activate it, run:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")

def ensure_pip(venv_python):
    """Ensure pip is installed/upgraded in the virtual environment."""
    print("\n Ensuring pip is installed/upgraded in the virtual environment...")
    subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)

def install_requirements(venv_python):
    """Installs dependencies from requirements.txt using the venv's Python."""
    print("\n Installing dependencies from requirements.txt...")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def check_env_file():
    """Ensures that .env exists, or creates a copy from .env.example."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    env_example_path = os.path.join(PROJECT_ROOT, ".env.example")

    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            print("\n Creating .env from .env.example...")
            if sys.platform == "win32":
                subprocess.run(["copy", env_example_path, env_path], shell=True)
            else:
                subprocess.run(["cp", env_example_path, env_path], check=True)
        else:
            print("\n WARNING: .env.example is missing! Create a .env file manually.")

def check_data_file():
    """Ensures that the dataset exists before running the project."""
    if not os.path.exists(DATA_FILE):
        print(f"\n WARNING: Data file not found: {DATA_FILE}")
        print("   Make sure you have the correct dataset in the /data folder.")

def main():
    print("\n Setting up your project...")

    create_virtualenv()                 # Create venv first
    venv_python = get_venv_python()      # Get the new venv's python path
    ensure_pip(venv_python)              # Use venv python to ensure pip is upgraded
    install_requirements(venv_python)    # Install dependencies with the venv python
    check_env_file()
    check_data_file()

    print("\n Setup complete! You are ready to go.")

if __name__ == "__main__":
    main()
    sys.exit(0)
