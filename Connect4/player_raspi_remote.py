from time import sleep
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
        self.icon = super().register_in_game()         # call method of Parent Class (Player_Local)
        if self.icon == 'X':
            self.icon = (0, 255, 0)
        elif self.icon == 'O':
            self.icon = (0, 0, 255)
       
    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        status = super().get_game_status() # call method of Parent Class (Player_Remote)
        sleep(1)
        return status["active_player"] == str(self.id)
     
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        for i in range(8):
            if i == column:
                self.sense.set_pixel(i, 0, self.icon)
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
        col = 0
        self.visualize_choice(col)
        while True:
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left' and col > 0:
                        col -= 1
                    elif event.direction == 'right' and col < 7:
                        col += 1
                    elif event.direction == 'middle':
                        response = requests.post(f"{self.api_url}/connect4/make_move", json={"column": col + 1,"player_id": str(self.id)})
                        if response.status_code == 200:
                            data = response.json()
                            self.success = data
                            if self.success:
                                return f"You made a move in column {col}"
                            else:
                                return f"Invalid move. Please try again."
                        else:
                            raise Exception("Failed to get game status")
                    self.visualize_choice(col)
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Remote Player
        """
        # Define Colors
        golden = (255, 236, 39)
        ruby = (255, 0, 64)
        
        status = super().get_game_status()
        if status["winner"]:
            self.visualize()
            sleep(0.5)
            print(f"Congratulations! Player {status["active_player"]} has won the game!")
            
            # Get the color of the winner
            if self.icon == (0, 0, 255):
                winner_color = (0, 255, 0)
            elif self.icon == (0, 0, 255):
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
            sleep(5)
            self.sense.clear()       
            
        elif status["turn"] == self.board_width * self.board_height:
            self.visualize()
            sleep(0.5)
            print("It's a draw")

            draw = [
            ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby,
            (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0),
            (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby, ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby, ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby, (0, 0, 0),
            ruby, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), ruby
            ]
            # Display the crown pattern
            self.sense.set_pixels(draw)
            sleep(5)
            self.sense.clear()      
        else:
            print("No win detected yet.")