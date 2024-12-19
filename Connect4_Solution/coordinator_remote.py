from time import sleep


class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI (raspi = False) or
        - playing over SenseHat (raspi = True). 

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (SenseHat):   Optional Local Instance of a SenseHat (if on Raspi)
    """

    def __init__(self, api_url: str, on_raspi: bool, bot:bool = False) -> None:
        """
        Initialize the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
            on_raspi (bool):    Indicates whether the game is running on a Raspberry Pi.
                                If True, initializes a Raspberry Pi player; otherwise, a regular player.
        """
        self.api_url = api_url

        # Import the appropriate player class based on the platform
        if on_raspi:
            from player_raspi_remote import Player_Raspi_Remote
            from sense_hat import SenseHat

            # Initialize the SenseHat and Raspberry Pi player
            self.sense = SenseHat()
            self.player = Player_Raspi_Remote(api_url=api_url, sense=self.sense)
        else:
        
        # bot not yet on raspi
            if bot:
                print(f"selected BOT")
                from player_bot_cli import Bot_Remote
                self.player = Bot_Remote(api_url=api_url)

            else:
                from player_remote import Player_Remote

                # Initialize a standard remote player
                self.player = Player_Remote(api_url=api_url)

        self.turn_number = -1

    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """
        active_icon = None
        while active_icon is None:
            active_icon, _, _, _ = self.player.get_game_status()
            print("Waiting for second player to connect...")
            sleep(1)

        print("--------- Game Started ----------- ")

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        # Register players in the game
        self.player.register_in_game()  

        self.wait_for_second_player()  # Wait until the second player is connected

        while True:

            # Get the current game status
            _, active_uuid, winner, turn_number = self.player.get_game_status()

            # Update the turn number and visualize the board if it's a new turn
            if self.turn_number < turn_number:
                self.turn_number += 1
                self.player.visualize()

            # Check if there's a winner
            if winner:
                print(f"Player {winner} won the game")

                if winner == self.player.icon:
                    # celebrate player win if you are the winner
                    self.player.celebrate_win()

                break  # Exit the game loop

            # Make moves for the player if it's their turn
            if self.player.is_my_turn(active_uuid):
                made_move = False
                while not made_move:
                    made_move = self.player.make_move()
                    if not made_move:
                        print("Move was illegal. Please try again.")
            else:
                print("Waiting for the other player to make a move.")
                sleep(1)    # sleep a bit if not your turn

if __name__ == "__main__":
    api_url = "http://localhost:5000"  # Connect 4 API server URL
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    # pc_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url,
                                  on_raspi=False,
                                  bot = False)
    c_remote.play()
