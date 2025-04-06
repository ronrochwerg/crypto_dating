# Crypto Dating
## Overview

Crypto Dating is a project that combines cryptographic principles with a dating application concept. This repository contains the codebase for the project, including demo data generation, server setup, and a demonstration run.

## Requirements

- Python 3.8 (may work with later versions but a different openmined-psi wheel would have to be used)
- Recommended: A virtual environment to manage dependencies
- **Environment**: This project is designed to run in a Linux or WSL (Windows Subsystem for Linux) environment.

## Setup Instructions

1. **Clone the Repository**  
    Clone this repository to your local machine:
    ```bash
    git clone https://github.com/ronrochwerg/crypto_dating.git
    cd crypto_dating
    ```

2. **Set Up a Virtual Environment**  
    Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```

3. **Install Dependencies**  
    Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Generate Demo Data**  
    Run the script to generate demo data (fill in the data as specified by the script):
    ```bash
    python3 demo_data.py
    ```

2. **Start the Server**  
    Launch the server:
    ```bash
    python3 server.py
    ```

3. **Run the Demo**  
    In a separate terminal, execute the demo run script:
    ```bash
    python3 demo_run.py
    ```

## Notes

- Ensure all dependencies are installed before running the scripts.
- This project is specifically designed to run in a Linux or WSL environment. Running it in other environments may lead to unexpected issues.
- If you encounter issues, check the Python version and virtual environment setup.
