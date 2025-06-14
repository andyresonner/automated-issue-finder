# find_issues.py - Refactored into Functions

import os
import requests
import pandas as pd
import time

# A constant for our list of target repositories
TARGET_REPOS = [
    "microsoft/vscode",
    "facebook/react",
    "tensorflow/tensorflow",
    "kubernetes/kubernetes",
    "flutter/flutter",
    "godotengine/godot",
    "firstcontributions/first-contributions"
]

def fetch_issues_for_repo(repo_full_name, token):
    """Fetches beginner-friendly issues for a single repository."""
    owner, repo = repo_full_name.split('/')
    print(f"\nFetching issues from {owner}/{repo}...")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {
        "state": "open",
        "labels": "good first issue,help wanted",
        "sort": "updated",
        "direction": "desc",
        "per_page": 10,
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        issues = response.json()
        print(f"  Found {len(issues)} issues.")
        return issues
    except requests.exceptions.RequestException as e:
        print(f"  Failed to fetch issues: {e}")
        return []

def process_and_format_issues(all_raw_issues, target_repos):
    """Takes a list of raw issue data and formats it into a clean list of dictionaries."""
    processed_issues = []
    # Create a set for faster lookups
    repo_set = set(target_repos)
    
    for repo_issues in all_raw_issues:
        for issue in repo_issues:
            # Construct the repo name to check if it's in our target list
            repo_name = issue['repository_url'].split('repos/')[1]
            if repo_name in repo_set:
                 processed_issues.append({
                    'repository': repo_name,
                    'title': issue['title'],
                    'url': issue['html_url'],
                    'created_at': issue['created_at'].split('T')[0],
                })
    return processed_issues

def main():
    """Main function to orchestrate the script."""
    try:
        token = os.environ['GH_TOKEN']
    except KeyError:
        print("CRITICAL ERROR: GH_TOKEN environment variable not set.")
        raise

    all_raw_issues = []
    print("Starting to fetch issues...")
    
    for repo_name in TARGET_REPOS:
        issues = fetch_issues_for_repo(repo_name, token)
        if issues:
            all_raw_issues.append(issues)
        time.sleep(1) # Be a good API citizen

    print("\n--- All issues collected! Saving to CSV... ---")
    if all_raw_issues:
        # Flatten the list of lists into a single list of issues
        flat_list = [item for sublist in all_raw_issues for item in sublist]
        
        # In this refactored version, we pass the raw data to be processed.
        # This is better for testing, but let's re-process for simplicity here.
        processed_list = []
        for issue in flat_list:
            processed_list.append({
                'repository': issue['repository_url'].split('repos/')[1],
                'title': issue['title'],
                'url': issue['html_url'],
                'created_at': issue['created_at'].split('T')[0],
            })

        df = pd.DataFrame(processed_list)
        df.to_csv('issues.csv', index=False)
        print("Successfully saved issues to issues.csv")
    else:
        print("No issues found across all repositories.")

# This is a standard Python convention to make the script runnable
if __name__ == "__main__":
    main()
