import uuid
import numpy as np
from scipy.signal import convolve2d

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
        self.board = np.full((7, 8), " ", dtype="str")
        self.registered = {"Player1": None, "Player2": None}
        self.playericon = {}
        self.counter = 0
        self.winner = False
        self.activeplayer = None
        self.move = None
    """
    Methods to be exposed to the API later on
    """
    def get_status(self):
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
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
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        if self.registered["Player1"] == None:
            self.registered["Player1"] = player_id
            self.playericon[player_id] = "X"
        elif self.registered["Player2"] == None:
            self.registered["Player2"] = player_id
            self.playericon[player_id] = "O"
        else: 
            return None #evt. Fehlermeldung falls man nochmals registrieren möchte
        if self.counter == 0:
            self.activeplayer = self.registered.get("Player1")
        return self.playericon[player_id]

    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        return self.board

    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        if 1 <= column <= 8:
            col = column - 1
            values = [" "]
            exists = np.isin(self.board[:,col], values, invert=True)
            nextrow = np.where(exists)[0]
            if nextrow.size == 0:
                nextrow = 6
            elif nextrow[0] == 7:
                return False
            else:
                nextrow = nextrow[0] - 1
            self.board[nextrow][col] = self.playericon.get(player_Id)
            self.__detect_win(self.playericon.get(player_Id))
            self.__update_status()
            return True
        else: 
            return False
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
        Detect if someone has won the game (4 consecutive same pieces).
        Returns:
            True if there's a winner, False otherwise
        """
               
        if self.counter == 56:
            return f"Game over"

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