import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

COUNTRY = "Zimbabwe"
LIMIT = 50
README_FILE = "README.md"
MARKER_START = "<!-- START LEADERBOARD -->"
MARKER_END = "<!-- END LEADERBOARD -->"

def fetch_users_by_country(country, limit=10):
    query = f"location:{country}"
    url = f"https://api.github.com/search/users?q={query}&per_page={limit}&sort=followers&order=desc"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("items", [])

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def generate_leaderboard_md(users):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"**Last updated:** {now}  \n", f"| Rank | Username | Followers | Public Repos | Profile |"]
    lines.append("|------|----------|-----------|--------------|---------|")

    for i, user in enumerate(users, 1):
        username = user["login"]
        details = get_user_details(username)
        lines.append(
            f"| {i} | `{username}` | {details.get('followers', 0)} | {details.get('public_repos', 0)} | [🔗](https://github.com/{username}) |"
        )
    return "\n".join(lines)

def update_readme(leaderboard_md):
    with open(README_FILE, "r") as f:
        content = f.read()

    new_content = content.split(MARKER_START)[0] + MARKER_START + "\n" + leaderboard_md + "\n" + MARKER_END + content.split(MARKER_END)[1]
    
    with open(README_FILE, "w") as f:
        f.write(new_content)

def main():
    users = fetch_users_by_country(COUNTRY, LIMIT)
    leaderboard_md = generate_leaderboard_md(users)
    update_readme(leaderboard_md)

if __name__ == "__main__":
    main()
