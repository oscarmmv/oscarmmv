import requests
from datetime import datetime, timedelta
import re

def is_server_running():
    try:
        response = requests.get('http://localhost:3000/status')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def is_user_active(username):
    response = requests.get(f'https://api.github.com/users/{username}/events/public')
    events = response.json()

    github_active = False
    vscode_active = is_server_running()

    for event in events:
        if 'repo' in event and event['repo']['name'] == 'oscarmmv/oscarmmv':
            continue  

        event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if event_date > datetime.now() - timedelta(minutes=5):
            github_active = True

    return github_active, vscode_active

def update_readme(username, github_active, vscode_active):
    with open('README.md', 'r') as file:
        content = file.read()

    if github_active:
        content = re.sub(r'https://img.shields.io/static/v1\?label=GitHub&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=GitHub&message=Active&color=brightgreen', content)
    else:
        content = re.sub(r'https://img.shields.io/static/v1\?label=GitHub&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=GitHub&message=Inactive&color=lightgrey', content)
    if vscode_active:
        content = re.sub(r'https://img.shields.io/static/v1\?label=VSCode&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=VSCode&message=Active&color=skyblue', content)
    else:
        content = re.sub(r'https://img.shields.io/static/v1\?label=VSCode&message=\w+&color=\w+', 'https://img.shields.io/static/v1?label=VSCode&message=Inactive&color=lightgrey', content)

    with open('README.md', 'w') as file:
        file.write(content)

username = 'oscarmmv'
github_active, vscode_active = is_user_active(username)
update_readme(username, github_active, vscode_active)
