import time

from sense_hat import SenseHat

from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Local Player -> with some changed methods
            (uses Methods of Game and SenseHat)
    """

    def __init__(self, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players.
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        super().__init__(**kwargs)

        # Extract the SenseHat instance from kwargs
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")


        self.sense.clear()          # Clear LED matrix on init

        self.color:tuple = None         # set in register_in_game
        self.enemy_color:tuple = None    # set in register_in_game

    # override register in game
    def register_in_game(self):
        # first do normal register
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

    
    def visualize_choice(self, selected_column:int=None, toggle_on:bool = False)->None:
        """ 
        Visualize the choice and the board on the sense-hat

        Parameters:
            selected_column (int):  Optional Which is the currently selected column
            toggle_on (bool):       Optional, to toggle selection LED (LED on if True)
        """
        # list of icons
        board = self.game.get_board()

        # Colors for the LED matrix
        empty_color = [0, 0, 0]             # Black for empty spaces
        # selection_color = [255, 255, 0]   # Yellow for selected column
        selection_color = self.color        # own color but blinking

        # identify own and enemy icon
        enemy_icon = "X" if self.icon == "O" else "O"

        # board to visualize (64 x 3 list)
        led_matrix = []

        # First add row row of empty spaces (to be filled with choice)
        led_matrix.extend([empty_color] * 8)


        # Now add 8 by 7 board state
        for row in board:
            for cell in row:
                if cell == "":                      # empty cell
                    led_matrix.append(empty_color)
                elif cell == enemy_icon:            # enemy cell
                    led_matrix.append(self.enemy_color)  
                elif cell == self.icon:             # own cell
                    led_matrix.append(self.color)    

        
        # if on (during blinking)
        if toggle_on:
            # Highlight the selected column in the top row with yellow
            if 0 <= selected_column < self.board_width:
                led_matrix[selected_column] = selection_color  # Top row is the first 8 pixels

        # Display the current game board on the Sense HAT LED matrix
        self.sense.set_pixels(led_matrix)


    def visualize(self) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """

        # visualize board on Raspi (without col_choice)
        self.visualize_choice()     

        # visualize on CLI
        super().visualize()

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        col = 0  # Start column at 0
        selected = False
        toggle_on = True   # toggle state of select LED

        while not selected:
            
            toggle_on = not toggle_on     # Toggle LED
            
            
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

        # return selected column (like normal move)
        return col
    
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Remote player
        """
        # set sense screen to own color
        self.sense.clear(self.color)
        # also do CLI celebration
        super().celebrate_win()

