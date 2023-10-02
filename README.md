# System Data Management Project 

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Using the `make` Command](#using-the-make-command)  <-- Added section
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Description

The **System Data Management** is a web application designed to collect and manage data from various sources, providing users with a convenient way to access and download the data they need. This README provides an overview of the project, how to set it up, and how to use it.

## Features

- Collects and manages domestic and international data.
- Supports different data categories and sources.
- Provides a user-friendly interface for data selection and download.
- Allows customization and extension for additional data sources.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/downloads/) installed on your local machine.
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) framework installed. You can install it using pip: `pip install flask`
- [Streamlit](https://streamlit.io/) framework installed. You also can install Streamlit in your environment: `pip install streamlit`

### Installation

Open your cmd and type:

```bash
make install
````
### Using the `make` Command

To execute various tasks related to your project, you can use the `make` command in the Windows Command Prompt (CMD). Here's how:

1. **Ensure Make is Installed**:

   Before using the `make` command, ensure that it's installed on your system. You can install 'make' using Chocolatey by following the provided instructions in the [Installation](#installation) section.

2. **Open the Command Prompt**:

   Open the Command Prompt by pressing `Win + R`, typing `cmd`, and pressing Enter.

3. **Navigate to Your Project Directory**:

   Use the `cd` command to navigate to your project directory. Replace `YourUsername` and the path to match your project's location:

   ```bash
   cd C:\Users\YourUsername\YourProjectFolder
   ```

4. **Run Makefile Commands**:

   Run Makefile commands using the `make` command followed by the specific target or command you want to execute. For example:

   ```bash
   make install
   ```

   The available commands and their descriptions are defined in your project's Makefile.

5. **Review Output**:

   As you execute Makefile commands, the Command Prompt will display relevant information, including task execution details and any error messages.

6. **Exit the Command Prompt**:

   To exit the Command Prompt, either close the window or enter:

   ```bash
   exit
   ```

## Usage

### Configuration

Before running the application, you may need to configure certain settings:

- Configure data sources and categories in the application.
- Customize the web interface to match your branding.

### Running the Application

To run the application, follow these steps:

1. Make sure your virtual environment is activated.

2. Start the Flask development server:


1. Access the application in your web browser at `http://localhost:5000`.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Push your changes to your fork and create a pull request.

## License

This project is licensed under the Ministry License - see the [LICENSE](https://www.mlvt.gov.kh/) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The web framework used.
- [Selenium](https://selenium-python.readthedocs.io/) - The tool for scraping data



