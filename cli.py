"""Terminal interface for the dice game."""

from .domain import DiceGame


def main() -> None:
    game = DiceGame()
    print("Dice Game — roll a total of 7 to win!")

    while True:
        request = input("Press Enter to roll, or type q to quit: ").strip().lower()
        if request in {"q", "quit"}:
            print("Thanks for playing!")
            return

        result = game.roll()
        outcome = "You win!" if result.player_won else "You lose."
        print(
            f"You rolled {result.first_face} + {result.second_face} "
            f"= {result.total}. {outcome}"
        )
