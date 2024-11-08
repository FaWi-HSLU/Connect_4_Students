from game import Connect4
from player import Player

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
        
        # Register the player in the game and get the assigned icon
        self.icon = self.game.register_player(self.id)
        
        return self.icon

    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        status = self.game.get_status()  # Spielstatus abfragen
        return status["active_player"] == self.id

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
        """
        status = self.game.get_status()
                
        if isinstance(status, tuple):
            active_player, turn = status
            return {
                "active_player": active_player,
                "turn": turn,
                "winner": None
            }
        else:
            return {
                "active_player": status,
                "turn": None,
                "winner": status
            }

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            try:
                print(f'Player "{self.game.playericon[self.id]}" it\'s your turn!')
                col = int(input("Enter the column number you want to drop your coin in (1-8): "))
                move_valid = self.game.check_move(col, self.id)
                if move_valid == True:
                    print(f"Move successful! Coin placed in column {col}.")
                    return col
                elif move_valid == "Game over":
                    print("Game over. No more moves can be made.")
                    return col
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        # Aktuellen Zustand des Spielfelds abfragen
        board = self.game.get_board()
        
        # Spielfeld im Konsolenformat darstellen
        print("\nAktuelles Spielbrett:")
        print("  1   2   3   4   5   6   7   8")
        print("|" + "---|" * 8)
        
        for row in board:
            row_display = "| " + " | ".join(f"{cell}" for cell in row) + " |"
            print(row_display)
        
        print("|" + "---|" * 8)

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        status = self.game.get_status()
        if status["winner"]:
            self.visualize()
            print(f"Congratulations! Player {status['winner']} has won the game!")
            self.restart_game()
        else:
            print("No win detected yet.")
            
    def restart_game(self) -> bool:
        restart = input(f"Do you want to restart the game? [Y/N]: ")
        if restart == "Y":
            return True
        elif restart == "N":
            print(f"Thanks for playing Connect 4.")
            return False
        else: 
            restart = input(f"Please enter 'Y' or 'N'")