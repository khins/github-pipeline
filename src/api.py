import requests
from fastapi import HTTPException

GITHUB_API_BASE = "https://api.github.com"


def fetch_user(username: str) -> dict:
    """Fetch public profile information for a GitHub user."""
    response = requests.get(f"{GITHUB_API_BASE}/users/{username}", timeout=10)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="GitHub API error while fetching user data",
        )

    return response.json()


def fetch_repos(username: str) -> list[dict]:
    """Fetch public repositories for a GitHub user."""
    response = requests.get(f"{GITHUB_API_BASE}/users/{username}/repos", timeout=10)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="GitHub API error while fetching repositories",
        )

    return response.json()
