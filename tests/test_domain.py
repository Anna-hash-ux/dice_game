"""Tests for the dice game domain model."""

import unittest

from dice_game.domain import DiceGame, RollResult


class FixedRandomSource:
    def __init__(self, faces: list[int]) -> None:
        self._faces = iter(faces)

    def randint(self, a: int, b: int) -> int:
        face = next(self._faces)
        if not a <= face <= b:
            raise AssertionError("Requested face is outside the expected range.")
        return face


class RollResultTests(unittest.TestCase):
    def test_total_of_seven_is_a_win(self) -> None:
        result = RollResult(first_face=3, second_face=4)

        self.assertEqual(result.total, 7)
        self.assertTrue(result.player_won)

    def test_any_other_total_is_a_loss(self) -> None:
        result = RollResult(first_face=2, second_face=3)

        self.assertEqual(result.total, 5)
        self.assertFalse(result.player_won)

    def test_face_outside_standard_die_range_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RollResult(first_face=0, second_face=6)


class DiceGameTests(unittest.TestCase):
    def test_roll_uses_random_source_for_both_faces(self) -> None:
        game = DiceGame(FixedRandomSource([1, 6]))

        result = game.roll()

        self.assertEqual((result.first_face, result.second_face), (1, 6))
        self.assertTrue(result.player_won)


if __name__ == "__main__":
    unittest.main()
