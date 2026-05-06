import os
import sys

# Ensure the app can find the local modules if run from a different directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ui.main_window import AntigravityApp

def main():
    app = AntigravityApp()
    app.mainloop()

if __name__ == "__main__":
    main()
