import unittest
from unittest.mock import patch

from src.app import (
    app,
    get_analytics,
    get_repos,
    get_top_repos,
    get_user,
    root,
    sync_user_data,
)


class TestAppFunctions(unittest.TestCase):
    def test_root_returns_health_message(self) -> None:
        self.assertEqual(root(), {"message": "GitHub Pipeline API is running"})

    @patch("src.app.fetch_user")
    def test_get_user_returns_payload(self, mock_fetch_user) -> None:
        mock_fetch_user.return_value = {"login": "kevin", "id": 123}

        result = get_user("kevin")
        self.assertEqual(result, {"login": "kevin", "id": 123})
        mock_fetch_user.assert_called_once_with("kevin")

    @patch("src.app.fetch_repos")
    def test_get_repos_returns_payload(self, mock_fetch_repos) -> None:
        mock_fetch_repos.return_value = [{"name": "repo-one"}, {"name": "repo-two"}]

        result = get_repos("kevin")
        self.assertEqual(result, [{"name": "repo-one"}, {"name": "repo-two"}])
        mock_fetch_repos.assert_called_once_with("kevin")

    @patch("src.app.analyze_repos")
    @patch("src.app.fetch_repos")
    def test_get_analytics_uses_repos_and_transform(
        self, mock_fetch_repos, mock_analyze_repos
    ) -> None:
        repos = [{"name": "repo-one", "stargazers_count": 5}]
        analytics = {
            "total_repos": 1,
            "total_stars": 5,
            "total_forks": 0,
            "most_starred_repo": {"name": "repo-one", "stars": 5, "url": None},
        }
        mock_fetch_repos.return_value = repos
        mock_analyze_repos.return_value = analytics

        result = get_analytics("kevin")
        self.assertEqual(result, analytics)
        mock_fetch_repos.assert_called_once_with("kevin")
        mock_analyze_repos.assert_called_once_with(repos)

    def test_routes_are_registered(self) -> None:
        route_paths = {route.path for route in app.routes}
        self.assertIn("/", route_paths)
        self.assertIn("/user/{username}", route_paths)
        self.assertIn("/repos/{username}", route_paths)
        self.assertIn("/analytics/{username}", route_paths)
        self.assertIn("/top-repos/{username}", route_paths)
        self.assertIn("/sync/{username}", route_paths)

    @patch("src.app.top_starred_repos")
    @patch("src.app.fetch_repos")
    def test_get_top_repos_uses_repos_and_transform(
        self, mock_fetch_repos, mock_top_starred_repos
    ) -> None:
        repos = [{"name": "repo-one", "stargazers_count": 5}]
        top_repos = [{"name": "repo-one", "stars": 5, "url": None}]
        mock_fetch_repos.return_value = repos
        mock_top_starred_repos.return_value = top_repos

        result = get_top_repos("kevin")
        self.assertEqual(result, top_repos)
        mock_fetch_repos.assert_called_once_with("kevin")
        mock_top_starred_repos.assert_called_once_with(repos, limit=5)

    @patch("src.app.upsert_user_and_repos")
    @patch("src.app.fetch_repos")
    @patch("src.app.fetch_user")
    def test_sync_user_data_fetches_and_upserts(
        self, mock_fetch_user, mock_fetch_repos, mock_upsert
    ) -> None:
        db = object()
        user = {"id": 1, "login": "kevin"}
        repos = [{"id": 10, "name": "repo-one"}]
        sync_result = {"username": "kevin", "synced_user_id": 1, "repos_synced": 1}

        mock_fetch_user.return_value = user
        mock_fetch_repos.return_value = repos
        mock_upsert.return_value = sync_result

        result = sync_user_data("kevin", db)
        self.assertEqual(result, sync_result)
        mock_fetch_user.assert_called_once_with("kevin")
        mock_fetch_repos.assert_called_once_with("kevin")
        mock_upsert.assert_called_once_with(db, user, repos)


if __name__ == "__main__":
    unittest.main()
