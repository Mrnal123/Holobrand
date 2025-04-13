#!/usr/bin/env python
"""
HoloBrand Backend Test Runner

This script runs all tests for the HoloBrand backend.
It provides options for running specific test modules or all tests.

Usage:
    python run_tests.py [options]

Options:
    --all           Run all tests (default)
    --api           Run only API endpoint tests
    --layout        Run only layout generator tests
    --ai            Run only AI utils tests
    --github        Run only GitHub integration tests
    --openai        Run only OpenAI integration tests
    --verbose       Run tests with verbose output
"""

import sys
import os
import pytest

def main():
    # Ensure the test uploads directory exists
    os.makedirs('tests/test_uploads', exist_ok=True)
    
    # Default arguments
    pytest_args = ['tests/']
    
    # Process command line arguments
    if len(sys.argv) > 1:
        if '--api' in sys.argv:
            pytest_args = ['tests/test_api_endpoints.py']
        elif '--layout' in sys.argv:
            pytest_args = ['tests/test_layout_generator.py']
        elif '--ai' in sys.argv:
            pytest_args = ['tests/test_ai_utils.py']
        elif '--github' in sys.argv:
            pytest_args = ['tests/test_github_utils.py']
        elif '--openai' in sys.argv:
            pytest_args = ['tests/test_openai_utils.py']
    
    # Add verbose flag if requested
    if '--verbose' in sys.argv:
        pytest_args.append('-v')
    
    # Run the tests
    print("\n=== Running HoloBrand Backend Tests ===")
    print(f"Test modules: {', '.join(pytest_args)}\n")
    
    exit_code = pytest.main(pytest_args)
    
    # Print summary
    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. See above for details.")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())