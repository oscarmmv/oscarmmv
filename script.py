import requests
from datetime import datetime, timedelta
import re

def is_user_active(username):
    response = requests.get(f'https://api.github.com/users/{username}/events/public')
    events = response.json()

    github_active = False
    vscode_active = False

    for event in events:
        event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if event_date > datetime.now() - timedelta(days=1):
            github_active = True
            if 'VSCode' in event['repo']['name']:
                vscode_active = True

    return github_active, vscode_active

def update_readme(username, github_active, vscode_active):
    with open('README.md', 'r') as file:
        content = file.read()

    if github_active:
        content = re.sub(r'https://img.shields.io/static/v1\?label=GitHub&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=GitHub&message=Active&color=brightgreen', content)
    else:
        content = re.sub(r'https://img.shields.io/static/v1\?label=GitHub&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=GitHub&message=Inactive&color=lightgrey', content)
    if vscode_active:
        content = re.sub(r'https://img.shields.io/static/v1\?label=VSCode&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=VSCode&message=Active&color=brightgreen', content)
    else:
        content = re.sub(r'https://img.shields.io/static/v1\?label=VSCode&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=VSCode&message=Inactive&color=lightgrey', content)

    with open('README.md', 'w') as file:
        file.write(content)

username = 'oscarmmv'
github_active, vscode_active = is_user_active(username)
update_readme(username, github_active, vscode_active)
