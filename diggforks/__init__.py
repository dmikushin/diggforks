#!/usr/bin/env python3

import os
import requests
import sys
import subprocess
import re

def is_git_repo():
    return subprocess.call(['git', 'branch'], stderr=subprocess.STDOUT, stdout = subprocess.DEVNULL) == 0

def clone_forks(user, repo, token):
    url = f"https://api.github.com/repos/{user}/{repo}/forks"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)
    forks = response.json()
    for fork in forks:
        os.system(f"git remote add {fork['owner']['login']}_fork {fork['clone_url']}")
        os.system(f"git fetch {fork['owner']['login']}_fork")
        branches = subprocess.check_output(['git', 'branch', '-r']).decode('utf-8').split('\n')
        for branch in branches:
            if f"{fork['owner']['login']}_fork" in branch:
                branch_name = branch.split('/')[1].strip()
                os.system(f"git branch {fork['owner']['login']}_{branch_name} {fork['owner']['login']}_fork/{branch_name}")

def extract_github_details(url):
    pattern = r"github\.com[:/](.+)/([^\.]+)"
    match = re.search(pattern, url)
    if match:
        username, repository = match.groups()
        return username, repository
    else:
        return None, None

def get_git_remote_url():
    result = subprocess.run(['git', 'remote', '-v'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    lines = output.split('\n')
    for line in lines:
        if '(fetch)' in line:
            return line.split()[1]
    return None

def main():
    if not is_git_repo():
        print("Error: The current directory is not a Git repository.")
        sys.exit(1)
    url = get_git_remote_url()
    if url is None:
        print("Error: No remote URL found")
        sys.exit(1)
    else:
        username, repository = extract_github_details(url)
        if username is None or repository is None:
            print(f'Error: Invalid GitHub URL: {url}')
            sys.exit(1)
        else:
            with open('/home/marcusmae/.diggforks', 'r') as file:
                token = file.read().strip()
            print(f'Looking for forks of {repository} by {username}')
            clone_forks(username, repository, token)

if __name__ == '__main__':
    main()

