# Revius API

API service for Revius.cl

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Revius API is a service designed to provide data and functionalities for Revius.cl. It is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.12 based on standard Python type hints.

## Features

- Fast and efficient API built with FastAPI
- Easy to extend and maintain
- Supports asynchronous programming
- Automatic interactive API documentation

## Software and tools recommended
- VS Code
- Dev Container Extension
- Docker
- Pyenv (not mandatory, highly recommended tough)
- PgAdmin
- Autopep + Flake8 (Formatter & Linter)

## Installation

To install and run the Revius API locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/johansneirap/revius-api.git
    cd revius-api
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```
    or 
    ```sh
    fastapi dev app/main.py
    ```
5. Run in Dev Container (Recommended)
    - Open the project in VSCODE
    - Check notifications and press `Reopen in a container`
    - This will open the project in an isolated container executing VS Code from inside, allowing use te same environment for everyone participating in the project
    - You are ready to go! 🎉

## Usage

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

## Endpoints

Here are some of the main endpoints provided by the Revius API:

- `GET /`: Returns a welcome message.

For a full list of endpoints and their details, refer to the interactive API documentation.

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Create a new feature/fix branch
2. Make sure your branch is always being rebased by main
3. Make your changes
4. Commit your changes
5. Push changes to your branch
6. Open a Pull Request
7. Once the changes are revised, merge it using only rebase strategy

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
