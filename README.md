# Gmail Login Automation

This repository contains a Python script that automates the process of retrieving Gmail login credentials from a PostgreSQL database using SQLAlchemy and then automating the Gmail login process using Selenium. This script is designed to streamline and automate login tasks for Gmail, making it easier for users to access their email accounts programmatically.

## Features

- Establishes a connection to a PostgreSQL database to retrieve email credentials.
- Uses SQLAlchemy to interact with the database securely and efficiently.
- Utilizes Selenium WebDriver to automate the Gmail login process.
- Implements robust error handling and logging for smooth and reliable execution.
- Configures Chrome WebDriver with appropriate options for automation tasks.

## Prerequisites

- Python 3.x
- PostgreSQL database with a table named `gmail_credentials` containing columns for `email` and `password`.
- ChromeDriver installed and the path correctly set in the script.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/gmail-login-automation.git
    cd gmail-login-automation
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Update the `DB_URL` and `DRIVER_PATH` constants in the script with your PostgreSQL database connection details and the path to your ChromeDriver executable.

## Usage

1. Run the script:

    ```sh
    python gmail_login_automation.py
    ```

    The script will connect to the PostgreSQL database, retrieve the email and password, and then automate the login process to Gmail.

## Configuration

- **DB_URL:** Update this constant in the script with your PostgreSQL database connection details.
- **DRIVER_PATH:** Update this constant in the script with the path to your ChromeDriver executable.

## Error Handling and Logging

The script includes robust error handling and logging mechanisms to ensure smooth execution and easy troubleshooting. Logs will be printed to the console, providing information on the progress and any issues encountered during execution.

