# ALX Backend Python - Unittests and Integration Tests

This repository contains Python utilities and their corresponding unit tests as part of the ALX Backend Python curriculum.

## Contents

- `utils.py`: Contains utility functions including:
  - `access_nested_map`: Accesses values in nested dictionaries
  - `get_json`: Fetches JSON from a URL
  - `memoize`: A memoization decorator

- `test_utils.py`: Contains unit tests for the utility functions using:
  - Python's `unittest` framework
  - `parameterized` for test parameterization

## Requirements

- Python 3.8+
- `parameterized` package (`pip install parameterized`)

## Running Tests

To run all tests:
```bash
python3 -m unittest discover