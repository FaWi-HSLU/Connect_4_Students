from game import Connect4
from player import Player
import uuid


class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, game:Connect4) -> None:
        """ 
        Initialize a local player.
            Must Implement all Methods from Abstract Player Class

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.game = game
        if not self.game:
            raise ValueError("A Connect4 game instance must be provided")
        self.icon = None

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player a UUID and icon.

        Returns:
            str: The player's icon.
        """
        # Assign a UUID to the player
        self.uuid = str(uuid.uuid4())
        
        # Register the player in the game and get the assigned icon
        self.icon = self.game.register_player(self.uuid)
        
        return self.icon

    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        col = input("Enter the column number you want to drop your coin in: ")
        self.game.check_move(col, self.uuid)
        raise NotImplementedError(f"You need to write this code first")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")