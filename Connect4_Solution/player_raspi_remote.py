import time

from sense_hat import SenseHat

from player_remote import Player_Remote

class Player_Raspi_Remote(Player_Remote):
    """
    Remote Player using Raspberry Pi with Sense HAT.
    
    This player overrides:
        - make_move to use the joystick for move input.
        - visualize to use the LED matrix for visualizing the board.
    
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize the Raspberry Pi Remote Player with a Sense HAT instance.

        Parameters:
            api_url (str): Target API URL to connect to.
            sense (SenseHat): SenseHat instance for LED matrix and joystick input.

        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize parent class
        super().__init__(**kwargs)
        
        # Extract the SenseHat instance from kwargs
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

        # Clear LED matrix on initialization
        self.sense.clear()

        self.color:tuple = None         # set in register_in_game
        self.enemy_color:tuple = None    # set in register_in_game
        
        self.icon = None  # Set later by register()


    def register_in_game(self):
        """
        Override register_in_game from Parent Class.
            Also remember color
        """
        # do normal registering
        super().register_in_game()

        # now set colors
        player_X_color = [255,0,0]  # X is red
        player_O_color = [0,0,255]  # O is blue

        if self.icon == "X":
            self.color = player_X_color
            self.enemy_color = player_O_color
            print(f"You [{self.icon}] are red")
        else:
            self.color = player_O_color
            self.enemy_color = player_X_color
            print(f"You [{self.icon}] are blue")

    def visualize_choice(self, selected_column: int = None, toggle_on:bool = False):
        """
        Visualization logic using Sense HAT's LED matrix for the Connect 4 board.
        Maps the 8x7 Connect 4 board to the 8x8 LED matrix.
        
        If a selected_column is provided, it will highlight the column in the top row
        with a yellow pixel to show the player's current selection.
        """
        board = self.get_board()        # from parent (make API call)

        # Colors for the LED matrix
        empty_color = [0, 0, 0]          # Black for empty space
        #selection_color = [255,255,0]    # Yellow Color is blinkings
        selection_color = self.color     # Own Color is blinking
        
        # identify own and enemy icon
        enemy_icon = "X" if self.icon == "O" else "O"

        # Create the LED matrix array based on the board state
        led_matrix = []

        # Add an first row of empty spaces to fill the LED matrix
        led_matrix.extend([empty_color] * self.board_width)

        # now add 8 by 7 board
        for row in board:
            for cell in row:
                if cell == "":
                    led_matrix.append(empty_color)
                elif cell == enemy_icon:
                    led_matrix.append(self.enemy_color)     
                elif cell == self.icon:
                    led_matrix.append(self.color)           

        # if on (during blinking)
        if toggle_on:
            # Highlight the selected column in the top row with yellow
            if 0 <= selected_column < self.board_width:
                led_matrix[selected_column] = selection_color  # Top row is the first 8 pixels

        # Display the current game board on the Sense HAT LED matrix
        self.sense.set_pixels(led_matrix)


    def visualize(self):
        """
        Adjusted visualization for Raspi    
        """
        
        # just do visualization with no choice here
        self.visualize_choice()

    

    def make_move(self) -> bool:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.
        """
        col = 0  # Start column at 0
        selected = False
        toggle_on = True
        
        while not selected:

            toggle_on = not toggle_on       # toggle LED
            time.sleep(0.1)

            # Wait for joystick input
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        col = (col - 1) % self.board_width  # Move left, wrap around if needed
                    elif event.direction == 'right':
                        col = (col + 1) % self.board_width  # Move right, wrap around if needed
                    elif event.direction == 'middle':
                        selected = True  # Select the current column
                        break
        
            # Display current selection on the LED matrix (flashing column indicator)
            self.visualize_choice(selected_column=col, toggle_on = toggle_on)

        # use superclass to send the move
        super().make_move(col)

        # return success
        return True

    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Remote player
        """
        # set sense screen to own color
        self.sense.clear(self.color)
        # also do CLI celebration
        super().celebrate_win()
