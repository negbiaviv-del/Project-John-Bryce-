quickstart = run pip install pydantic and then python infra.py 

# DevOps Infrastructure Provisioning Tool

## Overview
This tool automates the process of defining virtual machines and installing services (like Nginx) using Python and Bash.

## Project Structure
- `src/`: Core logic and Machine class.
- `scripts/`: Bash scripts for service installation.
- `configs/`: JSON configuration files.
- `logs/`: Execution logs.

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

## Installing
1. pydandic 
pip install pydantic

## Permission
1. get permission for nginx.sh
chmod +x scripts/install_nginx.sh

## How to run
python3 main2.py 