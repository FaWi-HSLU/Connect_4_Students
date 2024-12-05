import requests
import uuid
from player import Player

class Player_Remote(Player):
    """
    Remote Player class to interact with the Connect 4 server.

    Attributes:
        id (UUID): Unique identifier for the player.
        icon: The player's icon used in the game. (set during registration)
        api_url (str): URL of the Connect 4 server.
    """

    def __init__(self, api_url: str) -> None:
        super().__init__()
        self.api_url = api_url

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        response = requests.post(f"{self.api_url}/connect4/register")
        if response.status_code == 200:
            data = response.json()
            self.icon = data["icon"]
            return self.icon
        else:
            raise Exception("Failed to register player")

    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        status = self.get_game_status()
        return status["active_player"] == str(self.id)

    def get_game_status(self) -> dict:
        """
        Get the game's current status.

        Returns:
            dict: The game's status.
        """
        response = requests.get(f"{self.api_url}/connect4/status")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to get game status")

    def make_move(self) -> int:
        """
        Prompt the player to make a move.

        Returns:
            int: The column chosen by the player for the move.
        """
        column = int(input(f"Player {self.icon}, enter the column (1-{self.board_width}) to drop your coin: "))
        response = requests.post(f"{self.api_url}/connect4/make_move", json={"player_id": str(self.id), "column": column})
        if response.status_code == 200:
            return column
        else:
            raise Exception("Invalid move")

    def visualize(self) -> None:
        """
        Visualize the current board state.
        """
        response = requests.get(f"{self.api_url}/connect4/board")
        if response.status_code == 200:
            board = response.json()
            for row in board:
                print(" | ".join(row))
                print("-" * (self.board_width * 4 - 1))
        else:
            raise Exception("Failed to get board state")

    def celebrate_win(self) -> None:
        """
        Players personal "celebration" on how to visualize a Win.
        """
        print(f"Player {self.icon} wins! Congratulations!")

# Example usage
if __name__ == "__main__":
    api_url = "http://localhost:5000"  # Connect 4 API server URL
    player = Player_Remote(api_url)
    player.register_in_game()
    player.visualize()