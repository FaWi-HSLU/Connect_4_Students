import time
import requests
from sense_hat import SenseHat
from player_remote import Player_Remote

class Player_Raspi_Remote(Player_Remote):
    """ 
    Remote Raspi Player 
        Same as Remote Player -> with some changed methods
            (uses Methods of SenseHat and html requests to communicate with the server)
    """
    def __init__(self, api_url: str) -> None:
        """ 
        Initialize a remote Raspi player with a shared SenseHat instance.

        Parameters:
            api_url (str): Address of the server.
            sense (SenseHat): SenseHat instance
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Remote)
        super().__init__(api_url)
        self.api_url = api_url
        self.sense = SenseHat()      
        # Clear the SenseHat
        self.sense.clear()

    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        response = requests.post(f"{self.api_url}/connect4/register", json={"player_id": str(self.id)})
        if response.status_code == 200:
            data = response.json()
            self.icon = data
            return self.icon
        else:
            raise Exception("Failed to register player")
        
    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        status = self.get_game_status()
        return status["active_player"] == str(self.id)
    
    def get_game_status(self) -> dict:
        """
        Get the game's current status.

        Returns:
            dict: The game's status.
        """
        response = requests.get(f"{self.api_url}/connect4/status")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to get game status")
    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        if self.icon == 'X':
            self.icon_color = (0, 255, 0)
        if self.icon == 'O':
            self.icon_color = (0, 0, 255)
        for i in range(8):
            if i == column:
                self.sense.set_pixel(i, 0, self.icon_color)
            else:
                self.sense.set_pixel(i, 0, (0, 0, 0))

    def visualize(self) -> None:
        """
        Override Visualization of Remote Player
            Also Visualize on the Raspi 
        """
        response = requests.get(f"{self.api_url}/connect4/board")
        board = response.json()
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell == 'X':
                    self.sense.set_pixel(x, y + 1, (0, 255, 0))  # Green for Player 1
                elif cell == 'O':
                    self.sense.set_pixel(x, y + 1, (0, 0, 255))  # Blue for Player 2
                else:
                    self.sense.set_pixel(x, y + 1, (0, 0, 0))  # Off for empty

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        column = 0
        self.visualize_choice(column)
        while True:
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left' and column > 0:
                        column -= 1
                    elif event.direction == 'right' and column < 7:
                        column += 1
                    elif event.direction == 'middle':
                        response = requests.post(f"{self.api_url}/connect4/make_move", json={"player_id": self.id, "column": column + 1})
                        if response.status_code == 200:
                            return column + 1
                        else:
                            print("Invalid move. Please try again.")
                self.visualize_choice(column)
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Remote Player
        """
        
        # Define Colors
        golden = (255, 236, 39)
        ruby = (255, 0, 64)
        
        response = requests.get(f"{self.api_url}/connect4/status")
        status = response.json()
        if status["winner"]:
            self.visualize()
            time.sleep(0.5)
            print(f"Congratulations! Player {status['winner']} has won the game!")
            
            # Get the color of the winner
            if self.icon == "X":
                winner_color = (0, 255, 0)
            elif self.icon == "O":
                winner_color = (0, 0, 255)
            
            crown = [
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), golden, (0, 0, 0), golden, golden, (0, 0, 0), golden, (0, 0, 0),
            (0, 0, 0), golden, golden, ruby, ruby, golden, golden, (0, 0, 0),
            (0, 0, 0), (0, 0, 0), golden, golden, golden, golden, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), winner_color, winner_color, winner_color, winner_color, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), winner_color, winner_color, winner_color, winner_color, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), winner_color, winner_color, winner_color, winner_color, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), winner_color, winner_color, winner_color, winner_color, (0, 0, 0), (0, 0, 0)
            ]

            # Display the crown pattern
            self.sense.set_pixels(crown)
            time.sleep(5)         
            self.restart_game()
            
        else:
            print("No win detected yet.")

    def restart_game(self) -> bool:
        """
        Ask the player if they want to restart the game using symbols.
        """
        self.sense.clear()

        # Define symbols
        redo_sign = [
            (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0),
            (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255),
            (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255),
            (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255),
            (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255),
            (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255),
            (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0)
        ]
        check_sign = [
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 255, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 255, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 255, 0), (0, 0, 0),
            (0, 255, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0),
            (0, 255, 0), (0, 255, 0), (0, 0, 0), (0, 255, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)
        ]

        cross_sign = [
            (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0),
            (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0),
            (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0)
        ]

        # Start with redo sign
        self.sense.set_pixels(redo_sign)

        while True:
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        self.sense.set_pixels(check_sign)
                        choice = "check"
                    elif event.direction == 'right':
                        self.sense.set_pixels(cross_sign)
                        choice = "cross"
                    elif event.direction == 'middle':
                        if choice == "check":
                            return True
                        elif choice == "cross":
                            self.sense.clear()
                            return False