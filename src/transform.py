def analyze_repos(repos: list[dict]) -> dict:
    """Build simple analytics from a GitHub repositories payload."""
    if not repos:
        return {
            "total_repos": 0,
            "total_stars": 0,
            "total_forks": 0,
            "most_starred_repo": None,
        }

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)
    most_starred = max(repos, key=lambda repo: repo.get("stargazers_count", 0))

    return {
        "total_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "most_starred_repo": {
            "name": most_starred.get("name"),
            "stars": most_starred.get("stargazers_count", 0),
            "url": most_starred.get("html_url"),
        },
    }


def top_starred_repos(repos: list[dict], limit: int = 5) -> list[dict]:
    """Return the top repositories sorted by stargazers_count descending."""
    sorted_repos = sorted(
        repos,
        key=lambda repo: repo.get("stargazers_count", 0),
        reverse=True,
    )

    return [
        {
            "name": repo.get("name"),
            "stars": repo.get("stargazers_count", 0),
            "url": repo.get("html_url"),
        }
        for repo in sorted_repos[:limit]
    ]
