import os
import sys
import subprocess


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "Craigslist_test.csv")

def install_requirements():
    """Installs dependencies from requirements.txt."""
    print("\n Installing dependencies from requirements.txt...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def create_virtualenv():
    """Creates and activates a virtual environment."""
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

def check_env_file():
    """Ensures that .env exists, or creates a copy from .env.example."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    env_example_path = os.path.join(PROJECT_ROOT, ".env.example")

    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            print("\n Creating .env from .env.example...")
            subprocess.run(["cp", env_example_path, env_path] if sys.platform != "win32" else ["copy", env_example_path, env_path], shell=True)
        else:
            print("\n WARNING: .env.example is missing! Create a .env file manually.")

def check_data_file():
    """Ensures that the dataset exists before running the project."""
    if not os.path.exists(DATA_FILE):
        print(f"\n WARNING: Data file not found: {DATA_FILE}")
        print("   Make sure you have the correct dataset in the /data folder.")

def main():
    """Runs the setup process."""
    print("\n Setting up your project...")

    install_requirements()
    create_virtualenv()
    check_env_file()
    check_data_file()

    print("\n Setup complete! You are ready to go.")

if __name__ == "__main__":
    main()
    sys.exit(0)