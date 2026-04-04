import subprocess
import time
import unittest
from pathlib import Path

import requests


class TestAppIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = "http://127.0.0.1:8765"
        project_root = Path(__file__).resolve().parents[1]
        cls.server = subprocess.Popen(
            [
                str(project_root / "venv/bin/python"),
                "-m",
                "uvicorn",
                "src.app:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8765",
                "--log-level",
                "warning",
            ],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        deadline = time.time() + 10
        last_error = None
        while time.time() < deadline:
            try:
                response = requests.get(f"{cls.base_url}/", timeout=1)
                if response.status_code == 200:
                    return
            except Exception as error:  # noqa: BLE001
                last_error = error
                time.sleep(0.2)

        raise RuntimeError(f"Uvicorn failed to start for tests: {last_error}")

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "server") and cls.server.poll() is None:
            cls.server.terminate()
            try:
                cls.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.server.kill()

    def test_root_endpoint_over_http(self) -> None:
        response = requests.get(f"{self.base_url}/", timeout=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "GitHub Pipeline API is running"})


if __name__ == "__main__":
    unittest.main()
