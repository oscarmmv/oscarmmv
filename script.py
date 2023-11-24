import requests
from datetime import datetime, timedelta
import re

def is_user_active(username):
    response = requests.get(f'https://api.github.com/users/{username}/events/public')
    events = response.json()

    for event in events:
        event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if event_date > datetime.now() - timedelta(days=1):
            return True

    return False

def update_readme(username, active):
    with open('README.md', 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write(re.sub(r'Active: \w+', f'Active: {active}', content))
        file.truncate()

username = 'oscarmmv'
active = is_user_active(username)
update_readme(username, active)