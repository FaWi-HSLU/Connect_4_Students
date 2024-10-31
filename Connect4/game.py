import uuid
import numpy as np
from scipy.ndimage import convolve


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
        self.board = np.full((7, 8), "", dtype="<U1")  # Initialize the board with empty strings
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
                "winner": self.activeplayer  # set the winner explicitly
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
            self.playericon[player_id] = "0"
        else: 
            return None #evt. Fehlermeldung falls man nochmals registrieren möchte
        return self.playericon[player_id]

    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        self.board = np.ndarray(shape=(7, 8), dtype="<U1")

        if self.activeplayer == self.registered.get("Player1"):
            self.board[self.move] = self.playericon.get(self.activeplayer)
            Connect4.__detect_win()
            Connect4.__update_status()
            Connect4.get_status()
        else:
            self.board[self.move] = self.playericon.get(self.activeplayer)
            Connect4.__detect_win()
            Connect4.__update_status()
            Connect4.get_status()
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
            values = ["X", "0"]
            exists = np.isin(self.board[:,col], values)
            nextrow = np.where(exists)[0] - 1
            self.move = (nextrow, col)
            if nextrow > 0:
                Connect4.get_board()
                return True
            elif nextrow == 0:
                return f"Game over"
            else:
                raise KeyError(f"This couldn't be")
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
        if Connect4.__detect_win() == True:
                self.winner = True
        else:
                # check the next players turn
            if self.counter % 2 == 0:
                self.activeplayer = self.registered.get("Player1")
            else:
                self.activeplayer = self.registered.get("Player2")
                # add a new turn
            self.counter += 1
    

    def __detect_win(self) -> bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        Returns:
            True if there's a winner, False otherwise
        """
        # Define the kernel for convolution to detect 4 in a row
        kernel = np.array([1, 1, 1, 1])

        # Check horizontal direction
        horizontal_kernel = kernel
        horizontal_convolution = convolve(self.board == self.playericon[self.activeplayer], horizontal_kernel, mode='constant', cval=0)
        if np.any(horizontal_convolution == 4):
            print(f"There is a winner for player {self.activeplayer} in horizontal direction")
            return True

        # Check vertical direction
        vertical_kernel = kernel[:, None]
        vertical_convolution = convolve(self.board == self.playericon[self.activeplayer], vertical_kernel, mode='constant', cval=0)
        if np.any(vertical_convolution == 4):
            print(f"There is a winner for player {self.activeplayer} in vertical direction")
            return True

        # Check diagonal (top-left to bottom-right) direction
        diagonal_tl_br_kernel = np.eye(4)
        diagonal_tl_br_convolution = convolve(self.board == self.playericon[self.activeplayer], diagonal_tl_br_kernel, mode='constant', cval=0)
        if np.any(diagonal_tl_br_convolution == 4):
            print(f"There is a winner for player {self.activeplayer} in diagonal (top-left to bottom-right) direction")
            return True

        # Check diagonal (bottom-left to top-right) direction
        diagonal_bl_tr_kernel = np.fliplr(np.eye(4))
        diagonal_bl_tr_convolution = convolve(self.board == self.playericon[self.activeplayer], diagonal_bl_tr_kernel, mode='constant', cval=0)
        if np.any(diagonal_bl_tr_convolution == 4):
            print(f"There is a winner for player {self.activeplayer} in diagonal (bottom-left to top-right) direction")
            return True

        # No winner found
        return False