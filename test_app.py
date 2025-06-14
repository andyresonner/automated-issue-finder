# test_app.py

import pytest
from find_issues import process_and_format_issues

def test_process_and_format_issues():
    """
    Tests if the function correctly processes a sample raw issue dictionary
    into the format we expect for our DataFrame.
    """
    # Create sample raw data that mimics the GitHub API response
    sample_raw_issues = [
        {
            'repo_full_name': 'test-owner/test-repo',
            'title': 'Test Issue Title',
            'html_url': 'https://github.com/test-owner/test-repo/issues/1',
            'created_at': '2025-06-15T12:00:00Z',
            'state': 'open' # Other data that should be ignored
        }
    ]

    # The expected clean output after processing
    expected_output = [
        {
            'repository': 'test-owner/test-repo',
            'title': 'Test Issue Title',
            'url': 'https://github.com/test-owner/test-repo/issues/1',
            'created_at': '2025-06-15'
        }
    ]

    # Call the function with our sample data
    actual_output = process_and_format_issues(sample_raw_issues)

    # Assert that the actual output matches our expectation
    assert actual_output == expected_output

def test_process_empty_list():
    """Tests if the function correctly handles an empty list of issues."""
    assert process_and_format_issues([]) == []
