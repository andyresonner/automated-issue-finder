# find_issues.py - Corrected to use the helper function

import os
import requests
import pandas as pd
import time

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
    # ... (This function remains exactly the same)
    owner, repo = repo_full_name.split('/')
    print(f"\nFetching issues from {owner}/{repo}...")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    params = {"state": "open", "labels": "good first issue,help wanted", "sort": "updated", "direction": "desc", "per_page": 10}
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        issues = response.json()
        print(f"  Found {len(issues)} issues.")
        # Add repo_full_name to each issue for later processing
        for issue in issues:
            issue['repo_full_name'] = repo_full_name
        return issues
    except requests.exceptions.RequestException as e:
        print(f"  Failed to fetch issues: {e}")
        return []

def process_and_format_issues(all_raw_issues):
    """Takes a flat list of raw issue data and formats it into a clean list of dictionaries."""
    processed_issues = []
    for issue in all_raw_issues:
        processed_issues.append({
            'repository': issue['repo_full_name'],
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
        all_raw_issues.extend(issues) # Use extend to create a flat list
        time.sleep(1)

    print("\n--- All issues collected! Processing and saving to CSV... ---")
    if all_raw_issues:
        # CORRECTED: Now we properly use our helper function
        processed_list = process_and_format_issues(all_raw_issues)
        df = pd.DataFrame(processed_list)
        df.to_csv('issues.csv', index=False)
        print("Successfully saved issues to issues.csv")
    else:
        print("No issues found across all repositories.")

if __name__ == "__main__":
    main()
