
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
        # Initialize base properties and board dimensions
        super().__init__()  

        # Read out kwargs for the API URL
        try:
            self.api_url: str = kwargs["api_url"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires an 'api_url' attribute")

        self.icon = None

    def register_in_game(self):
        """
        Register the player in the game by making a POST request to the API.
        """
        try:
            response = requests.post(f'{self.api_url}/connect4/register', json={'player_id': str(self.id)})
            response_data = response.json()

            if response.status_code == 200:
                self.icon = response_data['player_icon']
                print(f"You are Player [{self.icon}]")
            else:
                print(f"Error registering player: {response_data.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    def get_game_status(self) -> tuple:
        """
        Get the game's status.

        Returns:
            tuple: (active_icon, active_player, winner, turn_number)
        """
        try:
            response = requests.get(f'{self.api_url}/connect4/status')
            response_data: dict = response.json()
    
            # Ensure correct order for the returned tuple
            active_icon = response_data.get('active_icon')
            active_player = response_data.get('active_id')
            winner = response_data.get('winner')
            turn_number = response_data.get('turn_number')

            return (active_icon, active_player, winner, turn_number)

        except Exception as e:
            print(f"Failed to check turn: {e}")
            # Return a default value in case of an error
            return (None, None, None, None)

    def is_my_turn(self, active_uuid: str = None) -> bool:
        """
        Check if it's the player's turn by making a GET request to the API.
        Returns True if it's the player's turn, otherwise False.

        Parameters:
            active_uuid (str)     Optional: UUID of active player, if given no API call is made

        Returns:
            bool: If player is the active player
        """
        # If not given -> make call to get active ID
        if active_uuid is None:
            try:
                response = requests.get(f'{self.api_url}/connect4/status')
                response_data = response.json()
                active_uuid = response_data['active_id']
            
            except Exception as e:
                print(f"Failed to check turn: {e}")
                return False
            
        # if active id == own id -> return true
        return str(self.id) == active_uuid

    def make_move(self, col: int = None) -> bool:
        """
        Ask the player to select a column and send a move request to the API.
        
        Parameters:
            col (int): Optional: Which column to be selected (used by child classes)
        
        Returns:
            bool: Success of move
        """
        try:
            # Only select a column if none is given
            if col is None:
                col = int(input(f"Player [{self.icon}], select a column: "))

            # Make the check_move request
            response = requests.post(f'{self.api_url}/connect4/check_move', json={'column': col, 'player_id': str(self.id)})
            response_data = response.json()

            if response.status_code == 200 and response_data.get('success', False):
                print(f"Move successful! Player [{self.icon}] placed in column {col}")
                return True
            else:
                print(f"Error: {response_data.get('error', 'Move failed')}")
                return False
        except ValueError:
            print("Invalid input. Please enter a valid column number.")
            return False
        except Exception as e:
            print(f"Failed to make a move: {e}")
            return False
        

    def get_board(self) -> np.ndarray:
        """
        Get the current board state from the server.
        
        Returns:
            np.ndarray: The current board state as a NumPy array, or None if retrieval fails.
        """
        response = requests.get(f'{self.api_url}/connect4/board')
        if response.status_code == 200:
            response_data = response.json()
            board: list[str] = response_data["board"]
            return np.array(board).reshape((self.board_height, self.board_width))  # Use instance attributes
        else:
            print(f"Error: Failed to retrieve board. Status Code: {response.status_code}")
            return None

    def visualize(self):
        """
        Visualize the current board.
        """
        board: np.ndarray = self.get_board()

        # Visualize the board
        for row in range(board.shape[0]):
            # Print the top border for each row (except the first row)
            if row > 0:
                # Print horizontal line
                print(" _ " * (board.shape[1] + 3))
            
            # Print the row elements with | as borders
            row_str = " | ".join(board[row, :])
            print(f"| {row_str} |")

    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Remote player
        """
        print(f"I player [{self.icon}] won!")