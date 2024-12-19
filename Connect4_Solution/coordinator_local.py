from game import Connect4
from player import Player


class Coordinator_Local:
    """ 
    Coordinator for two Local players
        - either playing over CLI (raspi = False) or
        - playing over SenseHat (raspi = True). 

    This class manages the game flow, player registration, turn management, 
    and game status updates for local players.


    Attributes:
        game (Connect4):    Local Instance of a Connect4 Game
        player1 (Player):   Local Instance of a Player (Raspi or Normal)
        player2 (Player):   Local Instance of a Player (Raspi or Normal)
    """

    def __init__(self, on_raspi: bool, bot:bool=False) -> None:
        """
        Initialize the Coordinator_Local.

        Parameters:
            on_raspi (bool): Indicates whether the game is running on a Raspberry Pi.
                             If True, initializes a Raspberry Pi player; otherwise, initializes standard players.
        
            bot (bool):     Whether this player is a bot or not
        
        """
        self.game = Connect4()
        self.turn_number = -1

        # Initialize 2 players based on the platform
        if on_raspi:
            from player_raspi_local import Player_Raspi_Local
            from sense_hat import SenseHat
            
            self.sense = SenseHat() # same sense hat for both players

            self.player_1 = Player_Raspi_Local(game=self.game, sense=self.sense)
            self.player_2 = Player_Raspi_Local(game=self.game, sense=self.sense) 
        
        else:
            from player_local import Player_Local
            
            self.player_1 = Player_Local(game=self.game)

            if bot:
                from player_bot_local import Bot_Local
                self.player_2 = Bot_Local(game = self.game)
            else:
                self.player_2 = Player_Local(game=self.game)

    def play(self):
        """ 
        Main function to run the game with two local players.
        
        This method handles player registration, turn management, 
        and checking for a winner until the game concludes.
        """
        # Register both players
        self.player_1.register_in_game()
        self.player_2.register_in_game()
        players: list[Player] = [self.player_1, self.player_2]

        while True:
            # Get the current game status
            active_icon, active_uuid, winner, turn_number = self.game.get_status()

            # If a new turn has occurred, visualize the board
            if turn_number > self.turn_number:
                self.turn_number += 1
                players[0].visualize()  # Visualize for any player
            
            # Check if there's a winner
            if winner:
                print(f"Player {winner} won the game after {turn_number} turns")

                for player in players:
                    if player.icon == winner:
                        player.celebrate_win()

                break  # Exit the game loop
            
            # Make a move for the active player
            for player in players:            
                if player.id == active_uuid:
                    print(f"Move of [{active_icon}]")

                    while True:
                        col = player.make_move()
                        made_move = self.game.check_move(col, player.id)

                        if made_move:
                            break
                        else:
                            print("Move was illegal. Please try again.")



if __name__ == "__main__":
    c4 = Coordinator_Local(on_raspi=False, bot=True)
    c4.play()
