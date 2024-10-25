import uuid
import random
from enum import Enum
import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game  
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """
    
    def __init__(self) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create to (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
        """
        self.board = None
        self.registered = []
        self.counter = 0
        self.winner = False

    """
    Methods to be exposed to the API later on
    """
    def get_status(self):

        if self.winner == True:
            return self.activeplayer
        else:
            return self.activeplayer, self.counter
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
        """
    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        
        self.registered()



    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """



    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """

        if True:
            Connect4.__detect_win()
            Connect4.__update_status()
        
    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status (after each successful move)
            - active player
            - active ID
            - winner
            - turn_number
        """
        if Connect4.__detect_win() == True:
                self.winner = True
        else:
            if self.counter % 2 == 0:
                self.player == 1
                # active ID
            else:
                self.player == 2
                # active ID
            self.counter += 1
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    
        # TODO
        raise NotImplementedError(f"You need to write this code first")