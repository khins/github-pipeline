from sqlalchemy.orm import Session

from src.models import Repo, User


def upsert_user_and_repos(db: Session, user_data: dict, repos_data: list[dict]) -> dict:
    user = User(
        github_id=user_data["id"],
        login=user_data.get("login", ""),
        name=user_data.get("name"),
        followers=user_data.get("followers", 0),
        following=user_data.get("following", 0),
        public_repos=user_data.get("public_repos", 0),
        html_url=user_data.get("html_url"),
    )
    db.merge(user)

    for repo_data in repos_data:
        repo = Repo(
            github_id=repo_data["id"],
            user_github_id=user_data["id"],
            name=repo_data.get("name", ""),
            full_name=repo_data.get("full_name"),
            stargazers_count=repo_data.get("stargazers_count", 0),
            forks_count=repo_data.get("forks_count", 0),
            language=repo_data.get("language"),
            html_url=repo_data.get("html_url"),
            updated_at=repo_data.get("updated_at"),
        )
        db.merge(repo)

    db.commit()

    return {
        "username": user_data.get("login"),
        "synced_user_id": user_data["id"],
        "repos_synced": len(repos_data),
    }
