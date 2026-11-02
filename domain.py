"""Domain model and rules for the dice game."""

import random
from dataclasses import dataclass
from typing import Protocol


class RandomSource(Protocol):
    """Source of random die faces."""

    def randint(self, a: int, b: int) -> int: ...


@dataclass(frozen=True)
class RollResult:
    """The two die faces and outcome for one roll."""

    first_face: int
    second_face: int

    def __post_init__(self) -> None:
        for face in (self.first_face, self.second_face):
            if not 1 <= face <= 6:
                raise ValueError("Die faces must be between 1 and 6.")

    @property
    def total(self) -> int:
        return self.first_face + self.second_face

    @property
    def player_won(self) -> bool:
        return self.total == 7


class DiceGame:
    """Roll two standard six-sided dice and return their result."""

    def __init__(self, random_source: RandomSource | None = None) -> None:
        self._random_source = (
            random_source if random_source is not None else random.Random()
        )

    def roll(self) -> RollResult:
        """Roll both dice once."""
        return RollResult(
            first_face=self._random_source.randint(1, 6),
            second_face=self._random_source.randint(1, 6),
        )
