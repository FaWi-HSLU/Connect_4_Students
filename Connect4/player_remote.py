
import requests
import numpy as np

from player import Player

class Player_Remote(Player):
    """ 
    Remote Player (uses API calls to interact with the Connect 4 server).
    
    Attributes:
        api_url (str): The base URL of the Connect 4 API server.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize the player with the provided API URL.

        Parameters:
            api_url (str): The base URL of the Connect 4 API server (e.g., http://localhost:5000).
        
        Raises:
            ValueError: If 'api_url' is not provided in kwargs.
        """
        # Initialize base properties and board dimensions of the normal Player
        super().__init__()  

        # Read out kwargs for the API URL (if kwargs are used)
        try:
            self.api_url: str = kwargs["api_url"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires an 'api_url' attribute")

        # TODO: init the rest

    def register_in_game(self):
        """
        Register the player in the game by making a POST request to the API.
        """
        
        # TODO: 

    def get_game_status(self) -> tuple:
        """
        Get the game's status. By sending a GET request to the Game Server, then read out the correct values

        Returns:
            tuple: (active_icon, active_player, winner, turn_number)
        """
        # TODO

    def is_my_turn(self) -> bool:
        """
        Check if it's the player's turn by making a GET request to the API.
        Returns True if it's the player's turn, otherwise False.

        Returns:
            bool: If player is the active player
        """
        
        # TODO: implement

    def make_move(self, col: int = None) -> bool:
        """
        Ask the player to select a column and send a POST request of it to the API.
        
        Parameters:
            col (int): Optional: Which column to be selected (used by child classes)
        
        Returns:
            bool: Success of move
        """
        
        # TODO: implement
        

    def get_board(self) -> np.ndarray:
        """
        Get the current board state from the server.
        Uses a GET request to get the Board,
        Then formats the content of the message correctls
        
        Returns:
            np.ndarray: The current board state as a NumPy array, or None if retrieval fails.
        """
        
        # TODO


    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Remote player
        """
        # TODO