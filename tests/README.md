# HoloBrand Backend Testing Guide

This guide explains how to set up and run tests for the HoloBrand backend. The test suite covers all major components of the backend, including API endpoints, layout generation, image processing, GitHub integration, and OpenAI personalization.

## Test Structure

The test suite is organized into the following modules:

- **API Endpoint Tests** (`test_api_endpoints.py`): Tests for all Flask API endpoints, including file upload, layout generation, 3D preview, and GitHub integration endpoints.
- **Layout Generator Tests** (`test_layout_generator.py`): Tests for the layout generation functionality, including style analysis, color palette generation, and 3D preview data generation.
- **AI Utils Tests** (`test_ai_utils.py`): Tests for image processing and analysis, including dominant color extraction, brand style analysis, and layout recommendations.
- **GitHub Integration Tests** (`test_github_utils.py`): Tests for GitHub API integration, including repository listing and searching.
- **OpenAI Integration Tests** (`test_openai_utils.py`): Tests for OpenAI API integration, including layout enhancement and style description generation.

## Setup

1. Install the required testing dependencies:

```bash
pip install pytest pytest-cov
```

2. Make sure your environment variables are set up correctly for testing. For local testing, you can use mock values:

```bash
# For Windows
set OPENAI_API_KEY=test_key
set GITHUB_TOKEN=test_token

# For Linux/Mac
export OPENAI_API_KEY=test_key
export GITHUB_TOKEN=test_token
```

## Running Tests

You can run all tests or specific test modules using the provided `run_tests.py` script:

```bash
# Run all tests
python run_tests.py --all

# Run only API endpoint tests
python run_tests.py --api

# Run only layout generator tests
python run_tests.py --layout

# Run only AI utils tests
python run_tests.py --ai

# Run only GitHub integration tests
python run_tests.py --github

# Run only OpenAI integration tests
python run_tests.py --openai

# Run tests with verbose output
python run_tests.py --verbose
```

Alternatively, you can use pytest directly:

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/test_api_endpoints.py

# Run with coverage report
pytest --cov=. tests/
```

## Test Coverage

The test suite aims to cover:

- **Unit Tests**: Testing individual functions and methods in isolation.
- **Integration Tests**: Testing the interaction between different components.
- **API Tests**: Testing the HTTP endpoints and their responses.
- **Error Handling**: Testing how the application handles errors and edge cases.

## Mocking External Dependencies

The tests use mocking to simulate external dependencies like:

- **OpenAI API**: Mocked to avoid actual API calls during testing.
- **GitHub API**: Mocked to simulate repository data without real API calls.
- **File System**: Test uploads are stored in a separate test directory.

## Adding New Tests

When adding new features to the backend, follow these guidelines for testing:

1. Create unit tests for new functions and methods.
2. Update integration tests if the feature interacts with other components.
3. Add API tests for new endpoints.
4. Test both successful scenarios and error cases.
5. Use mocking for external dependencies.

## Continuous Integration

For CI/CD pipelines, you can run the tests with:

```bash
pytest --cov=. --cov-report=xml tests/
```

This will generate a coverage report that can be used by CI tools to track test coverage over time.