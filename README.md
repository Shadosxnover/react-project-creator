# React Project Creator

A desktop application to quickly create and configure React projects with a user-friendly interface.

## Features

- Create React projects using either **Vite** or **Create React App**
- Support for **JavaScript** or **TypeScript** projects
- One-click installation of common React libraries and dependencies
- Automatic terminal launching with development server
- Cross-platform support for Windows, macOS, and Linux

## Installation

### Requirements
- Python 3.8+
- Node.js and npm installed and in your PATH

### Setup

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

### Executable

You can also download the standalone executable from the releases section, which doesn't require Python to be installed.

## Usage

1. Select your project type (Vite or Create React App)
2. Enter a project name
3. Choose a location where the project will be created
4. Select JavaScript or TypeScript
5. Choose any additional libraries to install
6. Click "Create Project"

The application will:
- Create the React project with the selected options
- Install all selected dependencies
- Optionally open a terminal with the development server running

## Troubleshooting

- **NPM not found**: Make sure Node.js is installed and in your PATH
- **Terminal doesn't open**: The app will create a launcher script in your project folder that you can run manually
- **Permission errors**: Make sure you have write permissions to the selected project directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT