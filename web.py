"""Browser interface for the dice game."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .domain import DiceGame


PAGE = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dice Game</title>
    <style>
      :root { color-scheme: dark; font-family: system-ui, sans-serif; }
      * { box-sizing: border-box; }
      body {
        min-height: 100vh; margin: 0; display: grid; place-items: center;
        background: radial-gradient(ellipse at top, #263b63, #101827 70%);
        color: #f5f7fb;
      }
      main {
        width: min(92vw, 430px); padding: 2.5rem; text-align: center;
        background: #18243a; border: 1px solid #344562; border-radius: 24px;
        box-shadow: 0 24px 80px #080d18aa;
      }
      h1 { margin: 0; font-size: 2.25rem; }
      p { color: #b8c5d9; }
      .dice { display: flex; justify-content: center; gap: 1rem; margin: 2rem 0; }
      .die {
        display: grid; place-items: center; width: 82px; height: 82px;
        border-radius: 18px; background: #f5f7fb; color: #18243a;
        font-size: 2.7rem; font-weight: 750;
      }
      button {
        width: 100%; padding: 0.9rem 1.2rem; border: 0; border-radius: 12px;
        background: #78e0b5; color: #10251e; font: inherit; font-weight: 700;
        cursor: pointer;
      }
      button:hover { background: #9af0ce; }
      button:focus-visible { outline: 3px solid white; outline-offset: 3px; }
      button:disabled { cursor: wait; opacity: 0.7; }
      #result { min-height: 1.5em; margin-bottom: 0; font-weight: 650; }
      #result.win { color: #78e0b5; }
      #result.loss, #result.error { color: #ff9a9a; }
    </style>
  </head>
  <body>
    <main>
      <h1>Dice Game</h1>
      <p>Roll two dice. Get a total of 7 to win.</p>
      <div class="dice" aria-label="Dice result">
        <span class="die" id="die-one" aria-label="First die">?</span>
        <span class="die" id="die-two" aria-label="Second die">?</span>
      </div>
      <button id="roll" type="button">Roll the dice</button>
      <p id="result" aria-live="polite">Ready when you are.</p>
    </main>
    <script>
      const button = document.querySelector("#roll");
      const result = document.querySelector("#result");
      button.addEventListener("click", async () => {
        button.disabled = true;
        result.className = "";
        result.textContent = "Rolling…";
        try {
          const response = await fetch("/roll", { method: "POST" });
          if (!response.ok) throw new Error("The roll could not be completed.");
          const roll = await response.json();
          document.querySelector("#die-one").textContent = roll.first_face;
          document.querySelector("#die-two").textContent = roll.second_face;
          result.textContent = `Total: ${roll.total}. ${
            roll.player_won ? "You win!" : "You lose."
          }`;
          result.className = roll.player_won ? "win" : "loss";
        } catch (error) {
          result.textContent = error.message;
          result.className = "error";
        } finally {
          button.disabled = false;
        }
      });
    </script>
  </body>
</html>
"""


class DiceGameHandler(BaseHTTPRequestHandler):
    """Serve the game page and a roll endpoint."""

    game = DiceGame()

    def do_GET(self) -> None:
        if self.path != "/":
            self.send_error(404)
            return

        content = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        if self.path != "/roll":
            self.send_error(404)
            return

        result = self.game.roll()
        content = json.dumps(
            {
                "first_face": result.first_face,
                "second_face": result.second_face,
                "total": result.total,
                "player_won": result.player_won,
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> None:
    """Start the local web server."""
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DiceGameHandler)
    print("Dice Game is running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dice Game.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
