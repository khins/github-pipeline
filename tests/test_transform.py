import unittest

from src.transform import top_starred_repos


class TestTransform(unittest.TestCase):
    def test_top_starred_repos_returns_sorted_and_limited(self) -> None:
        repos = [
            {"name": "repo-a", "stargazers_count": 2, "html_url": "http://a"},
            {"name": "repo-b", "stargazers_count": 10, "html_url": "http://b"},
            {"name": "repo-c", "stargazers_count": 0, "html_url": "http://c"},
            {"name": "repo-d", "stargazers_count": 8, "html_url": "http://d"},
            {"name": "repo-e", "stargazers_count": 4, "html_url": "http://e"},
            {"name": "repo-f", "stargazers_count": 1, "html_url": "http://f"},
        ]

        result = top_starred_repos(repos, limit=5)

        self.assertEqual(len(result), 5)
        self.assertEqual([repo["name"] for repo in result], ["repo-b", "repo-d", "repo-e", "repo-a", "repo-f"])
        self.assertEqual(result[0]["stars"], 10)

    def test_top_starred_repos_handles_empty_input(self) -> None:
        self.assertEqual(top_starred_repos([], limit=5), [])


if __name__ == "__main__":
    unittest.main()
