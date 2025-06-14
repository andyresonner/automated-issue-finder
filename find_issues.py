# Final Python Script for GitHub Actions

import os
import requests
import pandas as pd
import time

# Get the GitHub token from environment variables
try:
    token = os.environ['GH_TOKEN']
except KeyError:
    print("ERROR: GH_TOKEN environment variable not set.")
    raise

# Define the LIST of repositories we want to check
target_repos = [
    "microsoft/vscode",
    "facebook/react",
    "tensorflow/tensorflow",
    "kubernetes/kubernetes",
    "flutter/flutter",
    "godotengine/godot",
    "firstcontributions/first-contributions" # A repo specifically for beginners
]

# Set up the request headers
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

all_issues = []
print("Starting to fetch issues...")

# Loop through each repository in our list
for repo_full_name in target_repos:
    owner, repo = repo_full_name.split('/')
    print(f"\nFetching issues from {owner}/{repo}...")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
        "labels": "good first issue,help wanted", # Check for two common labels
        "sort": "updated",
        "direction": "desc",
        "per_page": 10, # Limit to 10 per repo to keep the list fresh
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        issues = response.json()
        print(f"  Found {len(issues)} issues.")
        
        for issue in issues:
            all_issues.append({
                'repository': repo_full_name,
                'title': issue['title'],
                'url': issue['html_url'],
                'created_at': issue['created_at'].split('T')[0],
            })
    else:
        print(f"  Failed to fetch issues. Status code: {response.status_code}")
        
    time.sleep(1)

# Create the final DataFrame and save it to a CSV file
print("\n--- All issues collected! Saving to CSV... ---")
if all_issues:
    df = pd.DataFrame(all_issues)
    df.to_csv('issues.csv', index=False)
    print("Successfully saved issues to issues.csv")
else:
    print("No issues found across all repositories.")
