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
        status = self.game.get_status()  # Spielstatus abfragen
        return status["active_player"] == self.uuid

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
        
        try:
            col = int(input("Enter the column number you want to drop your coin in: "))
            
            # Zug überprüfen
            move_valid = self.game.check_move(col, self.uuid)
            
            if move_valid == True:
                print(f"Zug erfolgreich! Stein in Spalte {col} platziert.")
                return col
            elif move_valid == "Game over":
                print("Das Spiel ist vorbei!")
                return -1
            else:
                print("Ungültiger Zug. Wählen Sie eine andere Spalte.")
        
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl zwischen 1 und 8 ein.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        # Aktuellen Zustand des Spielfelds abfragen
        board = self.game.get_board()
        
        # Spielfeld im Konsolenformat darstellen
        print("\nAktuelles Spielbrett:")
        print(" 1  2  3  4  5  6  7  8")
        print("-" * 24)
        
        for row in board:
            row_display = " ".join(cell if cell else "." for cell in row)  # Leere Zellen durch "." ersetzen
            print(row_display)
        
        print("-" * 24)


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        if self.game._detect_win():
            print("Congratulations! You have won the game!")
            # Hier könnte eine Animation oder eine detaillierte Gewinneranzeige erfolgen
        else:
            print("The game is still ongoing.")