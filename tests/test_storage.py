import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db import Base
from src.models import Repo, User
from src.storage import upsert_user_and_repos


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def test_upsert_user_and_repos_creates_records(self) -> None:
        user_data = {
            "id": 100,
            "login": "kevin",
            "name": "Kevin",
            "followers": 10,
            "following": 4,
            "public_repos": 2,
            "html_url": "https://github.com/kevin",
        }
        repos_data = [
            {
                "id": 200,
                "name": "repo-one",
                "full_name": "kevin/repo-one",
                "stargazers_count": 7,
                "forks_count": 2,
                "language": "Python",
                "html_url": "https://github.com/kevin/repo-one",
                "updated_at": "2026-04-04T10:00:00Z",
            }
        ]

        with self.SessionLocal() as db:
            result = upsert_user_and_repos(db, user_data, repos_data)

            self.assertEqual(result["username"], "kevin")
            self.assertEqual(result["repos_synced"], 1)
            self.assertEqual(db.query(User).count(), 1)
            self.assertEqual(db.query(Repo).count(), 1)

    def test_upsert_user_and_repos_updates_existing_records(self) -> None:
        user_data = {"id": 101, "login": "kevin", "followers": 1, "following": 1}
        repos_data = [{"id": 201, "name": "repo-one", "stargazers_count": 3}]

        with self.SessionLocal() as db:
            upsert_user_and_repos(db, user_data, repos_data)
            upsert_user_and_repos(
                db,
                {"id": 101, "login": "kevin", "followers": 10, "following": 2},
                [{"id": 201, "name": "repo-one", "stargazers_count": 9}],
            )

            user = db.query(User).filter(User.github_id == 101).one()
            repo = db.query(Repo).filter(Repo.github_id == 201).one()
            self.assertEqual(user.followers, 10)
            self.assertEqual(repo.stargazers_count, 9)
            self.assertEqual(db.query(User).count(), 1)
            self.assertEqual(db.query(Repo).count(), 1)


if __name__ == "__main__":
    unittest.main()
