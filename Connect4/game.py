import uuid
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
        if self.winner == True:
            return self.activeplayer
        else:
            return self.activeplayer, self.counter
        
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
        else:
            self.board[self.move] = self.playericon.get(self.activeplayer)
            Connect4.__detect_win()
        return self.board

    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        if column >= 1 and column <= 8:
            col = column - 1
            values = ["X", "0"]
            exists = np.isin(self.board[:,col], values)
            nextrow = np.where(exists)[0]
            self.move = (nextrow, col)
            if nextrow > 0:
                Connect4.get_board(self.move)
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
                # check the next playersturn
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

        # Check the columns
        counter = 0

        for collen in range(self.board.shape[1]):
            for rowlen in range(self.board.shape[0]):
                if self.board[rowlen, collen] == self.playericon.get(self.activeplayer):
                    counter +=1
                    if counter == 4:
                        print(f"There is a winner in column {collen + 1}")
                        break
                else:
                    counter = 0

        # Check the rows
        for rowlen in range(self.board.shape[0]):
            for collen in range(self.board.shape[1]):
                if self.board[rowlen, collen] == self.playericon.get(self.activeplayer):
                    counter += 1
                    if counter == 4:
                        print(f"There is a winner in row {rowlen + 1}")
                        break
                else:
                    counter = 0

        # Check diagonal
        positions = [
            ((3,0), (4,1), (5,2), (6,3)),
            ((3,0), (2,1), (1,2), (0,3)),
            ((2,0), (3,1), (4,2), (5,3), (6,4)),
            ((4,0), (3,1), (2,2), (1,3), (0,4)),
            ((1,0), (2,1), (3,2), (4,3), (5,4), (6,5)),
            ((5,0), (4,1), (3,2), (2,3), (1,4), (0,5)),
            ((0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6)),
            ((6,0), (5,1), (4,2), (3,3), (2,4), (1,5), (0,6)),
            ((0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7)),
            ((6,1), (5,2), (4,3), (3,4), (2,5), (1,6), (0,7)),
            ((0,2), (1,3), (2,4), (3,5), (4,6), (5,7)),
            ((6,2), (5,3), (4,4), (3,5), (2,6), (1,7)),
            ((0,3), (1,4), (2,5), (3,6), (4,7)),
            ((6,3), (5,4), (4,5), (3,6), (2,7)),
            ((0,4), (1,5), (2,6), (3,7)),
            ((6,4), (5,5), (4,6), (3,7))
            ]

        for row, col in positions[0]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[1]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[2]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[3]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[4]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[5]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[6]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[7]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[8]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[9]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[10]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[11]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False
            
        for row, col in positions[12]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False

        for row, col in positions[13]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False

        for row, col in positions[14]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False

        for row, col in positions[15]:
            if self.board[row, col] == self.playericon.get(self.activeplayer):
                counter += 1
                if counter == 4:
                    print(f"There is a winner in diagonal {row + 1}")
                    return True
            else:
                counter = 0
                return False        