import uuid
import random

import numpy as np


class Connect4:
    
    
    def __init__(self) -> None:
        self.rows = 7
        self.columns = 8
        self.__board = np.empty(shape = (self.rows,self.columns), dtype="str")  # 8 columns by 7 rows filled with None (for SenseHat)
        
        self.__board[:] = " "               # replace every element with a space


        # Assigned when 2nd player registers
        self.__active_icon = None                         
        self.__active_id = None


        self.__available_icons = ["X", "O"]
        # TODO: maybe refactor
        self.game_id = uuid.uuid4()             # generate a random UID
        
        # players get registered here
        self.players = {
        }

        
        # player IDs
        self.player_1_id:uuid.UUID = None
        self.player_2_id:uuid.UUID = None

        self.__winner = False

        # start at Turn 0
        self.__turn_number = 0

    """
    Methods to be exposed to the API later on
    """
    def get_status(self) ->tuple[int,str,any]:
        """
        Get the game's status.

        Returns:
            tuple: (active_icon, active_id, winner, turn_number)
        """
        return self.__active_icon, self.__active_id, self.__winner, self.__turn_number

    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Register a player

        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if faile)
        """

        print(f"Player {player_id} just registered")
        
        # checks (when to do nothing)
        if len(self.players) >= 2 or (player_id in list(self.players.values())):
            return None
                
        # passed checks -> assign ICON
        icon = self.__available_icons[len(self.players)]
        self.players[icon] = player_id
        
        # when 2nd player enters: -> random start player
        if len(self.players) == 2:
            start_icon = random.choice(self.__available_icons)
            self.__active_id = self.players[start_icon]
            self.__active_icon = start_icon

        return icon


    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state 

        Returns:
            __board (np.ndarray):   (8 x 7 Array filled with values of (`X`,`O`,``))
        """
        return self.__board


    def check_move(self, column:int, player_Id:uuid.UUID):
        """ 
        Check move of a certain player 

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player Icon (X or O)
        """
        if self.__legal_move(column, player_Id):
            
            # find lowest column
            lowest_row = None
            for row in range(0,self.rows):                      # go "down" row by row (row 0 is at the top)
                if self.__board[row, column] == " ":            # last entry with nothing (at the bottom) 
                    lowest_row = row
    
           
            # write in player move to board
            self.__board[lowest_row,column] = self.__active_icon
            
            # update the status of the game
            self.__update_status()

            return True
        
        return False
        
    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status
            - active player
            - active ID
            - winner
            - turn_number
        """

        # increase turn number
        self.__turn_number += 1

        # detect win and write __winner
        self.__detect_win()
        
        # toggle active player
        self.__active_icon = "O" if self.__active_icon == "X" else "X"
        print(f"Active player is {self.__active_icon}")

        # new active ID
        self.__active_id = self.players[self.__active_icon]
        
        


    def __legal_move(self,column:int,player:uuid.UUID) -> bool:
        """ 
        Checks if the given move was legal

        Parameters:
            column (int):       Which column was selected for the drop
            player (uuid):      PlayerId
        """
        
        if player != self.__active_id:     # not correct player
            return False
        
        if (column < 0) or (column > 7) or (self.__board[0,column] != " "):       # column is full / wrong
            return False
        
        return True
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    
        # Check horizontal, vertical, and diagonal directions for any winner
        for row in range(self.rows):
            for col in range(self.columns):
                # Get the player mark at the current position
                player_mark = self.__board[row, col]
                if player_mark == " ":
                    continue  # Skip empty cells
                
                # Check horizontally (right)
                if col <= self.columns - 4 and \
                player_mark == self.__board[row, col + 1] == self.__board[row, col + 2] == self.__board[row, col + 3]:
                    self.__winner = player_mark
                    return True
                
                # Check vertically (down)
                if row <= self.rows - 4 and \
                player_mark == self.__board[row + 1, col] == self.__board[row + 2, col] == self.__board[row + 3, col]:
                    self.__winner = player_mark
                    return True
                
                # Check diagonal (down-right)
                if row <= self.rows - 4 and col <= self.columns - 4 and \
                player_mark == self.__board[row + 1, col + 1] == self.__board[row + 2, col + 2] == self.__board[row + 3, col + 3]:
                    self.__winner = player_mark
                    return True
                
                # Check diagonal (up-right)
                if row >= 3 and col <= self.columns - 4 and \
                player_mark == self.__board[row - 1, col + 1] == self.__board[row - 2, col + 2] == self.__board[row - 3, col + 3]:
                    self.__winner = player_mark
                    return True

        # If no winner is found, return False
        return False