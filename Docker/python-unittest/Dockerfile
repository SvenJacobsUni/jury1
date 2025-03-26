# A Dockerfile for a Python image with the custom test runner script (json_test_runner.py) installed
# and the AST analyzer script (python_ast_analyzer.py) installed

FROM python:alpine

# Copy the custom test runner script into the container at /usr/src/app
COPY CustomRunners/CustomTestRunner/json_test_runner.py /custom-test-runner/json_test_runner.py

# Copy the AST analyzer script into the container
COPY CustomRunners/AstAnalyzer/python_ast_analyzer.py /custom-ast-analyzer/python_ast_analyzer.py
