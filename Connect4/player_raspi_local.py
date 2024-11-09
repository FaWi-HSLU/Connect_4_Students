import time
from sense_hat import SenseHat
from game import Connect4
from player_local import Player_Local

class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Local Player -> with some changed methods
            (uses Methods of Game and SenseHat)
    """
    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        super().__init__(game)
        self.game = game
        if not self.game:
            raise ValueError("A Connect4 game instance must be provided")
        self.icon = None
              
        # Extract the SenseHat instance from kwargs  (only if SHARED instance)
        self.sense: SenseHat = kwargs.get("sense", None)
        if not self.sense:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")
                
        # Clear the SenseHat
        self.sense.clear()

    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        
        # first do normal register
        self.icon = super().register_in_game()         # call method of Parent Class (Player_Local)
        
        if self.icon == 'X':
            self.icon = (0, 255, 0)
        if self.icon == 'O':
            self.icon = (0, 0, 255)
    
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
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """

        # Visualize Board on Raspi
        board = self.game.get_board()
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell == 'X':
                    self.sense.set_pixel(x, y + 1, (0, 255, 0))  # Green for Player 1
                elif cell == 'O':
                    self.sense.set_pixel(x, y + 1, (0, 0, 255))  # Blue for Player 2
                else:
                    self.sense.set_pixel(x, y + 1, (0, 0, 0))  # Off for empty

        # OPTIONAL: also visualize on CLI
        super().visualize()

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
                if event.direction == 'left' and column > 0:
                    column -= 1
                elif event.direction == 'right' and column < 7:
                    column += 1
                elif event.direction == 'middle':
                    move_valid = self.game.check_move(column + 1, self.id)
                    if move_valid:
                        return column + 1
                    else:
                        print("Invalid move. Please try again.")
                self.visualize_choice(column)
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        
        # Define Colors
        golden = (255, 236, 39)
        ruby = (255, 0, 64)
        crown_pad = (171, 82, 59)
        
        status = self.game.get_status()
        if status["winner"]:
            self.visualize()
            time.sleep(0.5)
            print(f"Congratulations! Player {status['winner']} has won the game!")
            
            # Get the color of the winner
            if self.game.playericon[status["winner"]] == "X":
                winner_color = (0, 255, 0)
            elif self.game.playericon[status["winner"]] == "O":
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