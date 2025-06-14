import pandas as pd
import os

# Read the CSV file
try:
    df = pd.read_csv('issues.csv')
except FileNotFoundError:
    print("issues.csv not found. Exiting.")
    exit()

# Convert the DataFrame to a Markdown table
if not df.empty:
    markdown_table = df.to_markdown(index=False)
else:
    markdown_table = "No open issues found today."

# Read the README.md file
with open('README.md', 'r') as f:
    readme_content = f.read()

# Find the placeholder tags
start_tag = ""
end_tag = ""

start_index = readme_content.find(start_tag)
end_index = readme_content.find(end_tag)

# Replace the content between the tags
if start_index != -1 and end_index != -1:
    new_readme = (readme_content[:start_index + len(start_tag)] +
                  "\n" + markdown_table + "\n" +
                  readme_content[end_index:])

    # Write the updated content back to the README.md file
    with open('README.md', 'w') as f:
        f.write(new_readme)
    print("README.md has been successfully updated.")
else:
    print("Placeholder tags not found in README.md.")
