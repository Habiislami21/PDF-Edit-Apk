import os
import subprocess
import customtkinter

# Find the path where customtkinter is installed
ctk_path = os.path.dirname(customtkinter.__file__)

# Prepare the PyInstaller command
command = [
    "pyinstaller",
    "--noconfirm",           # Automatically overwrite existing build
    "--onedir",              # Create a one-folder bundle (better for large apps than onefile)
    "--windowed",            # Don't show the console window
    "--name=AntigravityPDF", # Name of the executable
    f"--add-data={ctk_path};customtkinter/", # Include customtkinter assets
    "main.py"                # Entry point
]

print("Starting build process...")
print("Running command:", " ".join(command))

# Run PyInstaller
try:
    subprocess.run(command, check=True)
    print("\nBuild completed successfully!")
    print("You can find your executable in the 'dist/AntigravityPDF' folder.")
except subprocess.CalledProcessError as e:
    print("\nError during build process. Please make sure pyinstaller is installed.")
    print("Run: pip install pyinstaller")
