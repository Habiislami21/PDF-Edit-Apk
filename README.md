# AntigravityPDF

AntigravityPDF is a robust, modular, and professional Python-based desktop application for PDF manipulation. It provides a clean and responsive user interface built with `customtkinter` to perform essential PDF operations seamlessly.

## Features

- **PDF Merger**: Combine multiple PDF files into a single document effortlessly.
- **PDF Splitter**: Extract specific pages or split a large PDF into multiple smaller files.
- **PDF Editor**: Perform page-level editing, including:
  - Rotating pages
  - Reordering pages
  - Deleting unwanted pages
- **Word Converter**: 
  - Convert PDF documents to Word (DOCX) format.
  - Convert Word (DOCX) documents to PDF format.

## Technologies Used

- **Python 3.x**
- **UI Framework**: [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern, dark-themed GUI.
- **PDF Processing**: 
  - [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
  - [pypdf](https://pypdf.readthedocs.io/en/stable/)
- **Document Conversion**: 
  - [pdf2docx](https://pypi.org/project/pdf2docx/)
  - [docx2pdf](https://pypi.org/project/docx2pdf/)
- **Image Processing**: [Pillow](https://python-pillow.org/)

## Project Structure

```text
Adobe_PDF_Edit/
│
├── core/               # Core business logic (editor, merger, splitter, converter)
├── models/             # Data models
├── services/           # External services and utility wrappers
├── ui/                 # UI components and main window definitions (CustomTkinter)
├── utils/              # Helper functions and utilities
│
├── main.py             # Application entry point
├── build.py            # Script to build the executable using PyInstaller
├── requirements.txt    # Python dependencies
└── AntigravityPDF.spec # PyInstaller spec file
```

## Installation

1. **Clone or download the repository:**
   Ensure you have the project files locally.

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application from source, run:

```bash
python main.py
```

## Building the Executable

You can compile the application into a standalone executable using the provided `build.py` script. This uses `PyInstaller` under the hood.

1. Ensure PyInstaller is installed:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

3. The compiled executable will be located in the `dist/AntigravityPDF` folder.

## License

This project is open-source and free to use.
