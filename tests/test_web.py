"""Tests for the dice game's web interface."""

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dice_game.web import DiceGameHandler


class WebInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DiceGameHandler)
        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_homepage_serves_game_interface(self) -> None:
        with urlopen(self.base_url) as response:
            page = response.read().decode("utf-8")

        self.assertEqual(response.status, 200)
        self.assertIn("Roll the dice", page)
        self.assertIn('fetch("/roll"', page)

    def test_roll_endpoint_returns_dice_and_outcome(self) -> None:
        request = Request(f"{self.base_url}/roll", method="POST")

        with urlopen(request) as response:
            roll = json.loads(response.read())

        self.assertEqual(response.status, 200)
        self.assertIn(roll["first_face"], range(1, 7))
        self.assertIn(roll["second_face"], range(1, 7))
        self.assertEqual(roll["total"], roll["first_face"] + roll["second_face"])
        self.assertEqual(roll["player_won"], roll["total"] == 7)

    def test_unknown_path_returns_not_found(self) -> None:
        with self.assertRaises(HTTPError) as error:
            urlopen(f"{self.base_url}/missing")

        self.assertEqual(error.exception.code, 404)
        error.exception.close()


if __name__ == "__main__":
    unittest.main()
