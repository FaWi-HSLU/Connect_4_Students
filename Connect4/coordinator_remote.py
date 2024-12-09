from time import sleep
import platform
import requests

class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI or
        - playing over SenseHat

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (SenseHat):   Optional Local Instance of a SenseHat (if on Raspi)
    """

    def __init__(self, api_url: str) -> None:
        """
        Initialize the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        """
        self.api_url = api_url


        if platform.system() == "Windows":
            from player_remote import Player_Remote
            self.player = Player_Remote(api_url=self.api_url)
        else:
            from player_raspi_remote import Player_Raspi_Remote
            self.player = Player_Raspi_Remote(api_url=self.api_url)

    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """
        while True:
            response = requests.get(f"{self.api_url}/connect4/status")
            status = response.json()
            if status["active_player"] is not None:
                print("Second player connected.")
                break
            else:
                print("Waiting for second player")

            sleep(1)

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        # Register player
        print("Registering players...")
        self.player.register_in_game()
        
        # Wait for the second player to connect
        self.wait_for_second_player()

        # Main game loop
        print("Starting main game loop...")
        while True:
            response = requests.get(f"{self.api_url}/connect4/status")
            status = response.json()
            if status["winner"] or status["turn"] == self.player.board_width * self.player.board_height:
                self.player.celebrate_win()
                break
            if self.player.is_my_turn():
                self.player.visualize()
                self.player.make_move()
                self.player.visualize()
                                                                     
# To start a game
if __name__ == "__main__":
    api_url = "http://127.0.1.1:5000"  # Connect 4 API server URL
    
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    # pc_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url)
    c_remote.play()