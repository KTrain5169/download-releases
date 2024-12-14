import requests


def fetch_releases(source, repo):
    if source == 'GitHub':
        url = f"https://api.github.com/repos/{repo}/releases"
    elif source == 'GitLab':
        url = f"https://gitlab.com/api/v4/projects/{repo.replace('/', '%2F')}/releases"
    else:
        return []

    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()
        return [release['name'] for release in releases]
    else:
        return []


def fetch_artifacts(source, repo, release):
    if source == 'GitHub':
        url = f"https://api.github.com/repos/{repo}/releases"
    elif source == 'GitLab':
        url = f"https://gitlab.com/api/v4/projects/{repo.replace('/', '%2F')}/releases"
    else:
        return []

    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()
        for rel in releases:
            if rel['name'] == release:
                return [asset['name'] for asset in rel['assets']]
    return []


def download_artifact(source, repo, artifact):
    if source == 'GitHub':
        url = f"https://api.github.com/repos/{repo}/releases/assets/{artifact}"
    elif source == 'GitLab':
        url = f"https://gitlab.com/api/v4/projects/{repo.replace('/', '%2F')}/releases/assets/{artifact}"
    else:
        return False

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(artifact, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    else:
        return False
