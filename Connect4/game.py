import uuid
import numpy as np
from scipy.signal import convolve2d

class Connect4:
    """
    Connect 4 Game Class

    This class defines the rules and state of a Connect 4 game, including:
        - What constitutes a win
        - Valid and invalid moves
        - The size of the playing field

    It also keeps track of the current game state, including:
        - The current state of the board
        - The active player
        - The turn counter
        - The winner, if any

    The class is used by the Coordinator to execute game methods.
    """
    
    def __init__(self) -> None:
        """ 
        Initialize a Connect 4 game.

        This method sets up the initial state of the game, including:
            - Creating an empty board
            - Initializing two non-registered players
            - Setting the turn counter to 0
            - Setting the winner to False
            - Setting the active player to None
        """
        self.board = np.full((7, 8), " ", dtype="str")
        self.registered = {"Player1": None, "Player2": None}
        self.playericon = {}
        self.counter = 0
        self.winner = False
        self.activeplayer = None
        self.move = None


    def get_status(self):
        """
        Get the game's status.
        
        Returns:
            dict: A dictionary containing the following keys:
            - active player (id or icon)
            - turn number
            - winner, if any
        """
        if self.winner:
            return {
                "active_player": None,
                "turn": self.counter,
                "winner": self.activeplayer
            }
        else:
            return {
                "active_player": self.activeplayer,
                "turn": self.counter,
                "winner": None
            }
        
    def register_player(self, player_id:uuid.UUID) -> str:
        """ 
        Register a player with a unique ID and assign a icon.
        
        Parameters:
            player_id (UUID): Unique ID of the player.

        Returns:
            str: Player Icon if registration is successful, otherwise an error message.
        """
        if self.registered["Player1"] == None:
            self.registered["Player1"] = player_id
            self.playericon[player_id] = "X"
        elif self.registered["Player2"] == None:
            self.registered["Player2"] = player_id
            self.playericon[player_id] = "O"
        else: 
            return "Game is already full" 
        if self.counter == 0:
            self.activeplayer = self.registered.get("Player1")
        return self.playericon[player_id]

    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state

        Returns:
            np.ndarray: The current state of the board.
        """
        return self.board

    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal and update the board.

        Parameters:
            column (int): Selected column of coin drop
            player_Id (uuid.UUID): ID of the player making the move.
            
        Returns:
            bool: True if the move is valid, False otherwise. 
        """
        if 1 <= column <= 8:
            col = column - 1
            for row in range(6, -1, -1):
                if self.board[row, col] == " ":
                    self.board[row, col] = self.playericon.get(player_Id)
                    self.__detect_win(self.playericon.get(player_Id))
                    self.__update_status()
                    return True
            return False
        else: 
            return False

    def __update_status(self):
        """ 
        Internal Method (for Game Logic)
        
        Update the game status after each successful move.
        
        Updates:
            - active player
            - active ID
            - winner
            - turn_number
        """
        if self.__detect_win(self.playericon.get(self.activeplayer)) == True:
            self.winner = True
        else:
            # add a new turn
            self.counter += 1
            # check the next players turn
            if self.counter % 2 == 0:
                self.activeplayer = self.registered.get("Player1")
            else:
                self.activeplayer = self.registered.get("Player2")
    

    def __detect_win(self, playericon) -> bool:
        """ 
        Detect if a player has won the game (4 consecutive same pieces).

        Parameters:
            playericon (str): The icon of the player to check for a win.

        Returns:
            bool: True if there's a winner, False otherwise.
        """         
        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.array([[1], [1], [1], [1]])
        diagonal_kernel_1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        diagonal_kernel_2 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
        
        binary_board = (self.board == playericon).astype(int)
            
        if (convolve2d(binary_board, horizontal_kernel, mode='valid').max() >= 4 or
            convolve2d(binary_board, vertical_kernel, mode='valid').max() >= 4 or
            convolve2d(binary_board, diagonal_kernel_1, mode='valid').max() >= 4 or
            convolve2d(binary_board, diagonal_kernel_2, mode='valid').max() >= 4):
            return True
        
        # No winner found
        return False
    
    def new_game(self) -> None:
        """ 
        Reset the game to start a new game.
        """
        self.board = np.full((7, 8), " ", dtype="str")
        self.counter = 0
        self.winner = None
        self.activeplayer = self.registered.get("Player1")