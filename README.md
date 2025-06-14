# Automated Open-Source Issue Finder

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automated-issue-finder-2ctekxkx28ubhazeeosavd.streamlit.app/)

**The Problem:** Finding a first open-source contribution is a major hurdle for new developers. Opportunities are scattered, and the search is a manual, time-consuming process.

**The Solution:** This project automates the entire discovery process. It acts as a dedicated service that:

*  **Scans Popular Repositories:** Queries the GitHub API across projects like `microsoft/vscode`, `facebook/react`, and `kubernetes/kubernetes` on a daily schedule.
*  **Filters for Opportunity:** Identifies and collects issues specifically labeled as `good first issue` or `help wanted`.
* **Centralizes the Data:** Compiles all findings into a single, clean list and automatically updates this README page with the results.

**The Impact:** Ultimately, this tool transforms a frustrating manual search into a reliable, automated feed, making it easier than ever to get started with open-source development.

---

### Latest Beginner-Friendly Issues

<!-- ISSUES_TABLE_START -->
*This table is automatically updated daily by a GitHub Action. The full, interactive list can be found on the live Streamlit app linked above.*
<!-- ISSUES_TABLE_END -->

---
*This project was built using Python, Pandas, Streamlit, and GitHub Actions.*
