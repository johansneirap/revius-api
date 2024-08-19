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

## Usage

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

## Endpoints

Here are some of the main endpoints provided by the Revius API:

- `GET /`: Returns a welcome message.

For a full list of endpoints and their details, refer to the interactive API documentation.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.