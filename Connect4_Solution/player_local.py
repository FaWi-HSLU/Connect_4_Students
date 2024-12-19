

from game import Connect4
from player import Player


class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, **kwargs) -> None:
        """ 
        Initialize a local player.

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.
        
        Raises:
            ValueError: If 'game' is not provided in kwargs.
        """
        super().__init__()  # Initialize id and icon from the abstract Player class

        try:
            self.game: Connect4 = kwargs["game"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'game' attribute")

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        self.icon = self.game.register_player(self.id)
        print(f"You are Player [{self.icon}]")
        return self.icon

    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        return self.game.get_status()[1] == self.id

    def get_game_status(self) -> tuple[str,str,bool,int]:
        """
        Get the game's current status.

        Returns:
            tuple: (active_icon, active_player, winner, turn_number).
        """
        return self.game.get_status()

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            try:
                col = int(input(f"Player [{self.icon}], make your move (enter column number):\t"))
                return col      # return correct value and break loop
            except ValueError:
                print("Invalid input. Please enter a valid column number.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        board = self.game.get_board()

        for row in range(self.game.rows):
            # Print the top border for each row (except the first row)
            if row > 0:
                print(" _ " * (self.game.columns + 3))
   
            # Print the row elements with | as borders
            row_str = " | ".join(board[row, :])
            print(f"| {row_str} |")


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """

        print(f"I Player [{self.icon}] won!")