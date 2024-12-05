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
            self.player1 = Player_Remote(api_url=self.api_url)
            self.player2 = Player_Remote(api_url=self.api_url)
        else:
            from player_raspi_remote import Player_Raspi_Remote
            from sense_hat import SenseHat

            self.sense = SenseHat()
            self.player1 = Player_Raspi_Remote(api_url=self.api_url, sense=self.sense)
            self.player2 = Player_Raspi_Remote(api_url=self.api_url, sense=self.sense)

    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """

        while True:
            response = requests.get(f"{self.api_url}/connect4/status")
            status = response.json()
            if status["active_player"]:
                print("Second player connected.")
                break
            sleep(1)

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        # Register both players
        print("Registering players...")
        self.player1.register_in_game()
        
        # Wait for the second player to connect
        self.wait_for_second_player()
        
        self.player2.register_in_game()

        # Main game loop
        print("Starting main game loop...")
        while True:
            for player in [self.player1, self.player2]:
                player.visualize()
                column = player.make_move()
                print(f"Player {player.id} made a move in column {column}")
                player.visualize()
                
                response = requests.get(f"{self.api_url}/connect4/status")
                status = response.json()
                if status["winner"]:
                    player.celebrate_win()
                    if player.restart_game():
                        self.new_game()
                    else:
                        return
                    
                elif status["turn"] == self.player1.board_width * self.player1.board_height:
                    if player.restart_game():
                        self.new_game()
                    else:
                        return
                    
                    
    def new_game(self):
        """
        Start a new game by resetting the board and status.
        """
        #TODO TODO TODO /connect4/new_game muss noch gemacht werden
        response = requests.post(f"{self.api_url}/connect4/new_game") 
        if response.status_code == 200:
            print("New game started.")
        else:
            print("Failed to start a new game.")

# To start a game
if __name__ == "__main__":
    api_url = "http://localhost:5000"  # Connect 4 API server URL
    
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    # pc_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url)
    c_remote.play()