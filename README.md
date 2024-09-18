# Health Checker Application

## Overview
This application monitors the availability of domains based on HTTP response codes and response latency. It calculates the hit ratio for each domain based on successful requests (`2xx` responses) that have a latency of less than 500 milliseconds.

## Features
- Configurable list of URLs in YAML format.
- Logs the hit ratio of each domain every 15 seconds to console.
- Thread pooling for efficient URL checking.
- Graceful shutdown on `Ctrl+C`.

## Prerequisites
- Python 3.7+ (Developed on 3.9.13)
- pip (Python package installer)

## Installation
1. Clone this repository.
2. Navigate to the project directory.

## Commands to be used in cmd:
    git clone https://github.com/Amey22s/domain-health-checker
    cd domain-health-checker

---

### How to Run the Application

1. **Install Dependencies**:
   - Run `pip install -r requirements.txt` to install the necessary libraries.
   
2. **Run the Application**:
   - Run `python health_checker.py <path-to-input-yaml-file>`.

3. **Access Logs**:
   - The logs will be printed to the console every 15 seconds, showing the availability of the domains.


P.S. In this case, `<path-to-input-yaml-file>` can be replaced with input.yaml which has the sample input file.

---
