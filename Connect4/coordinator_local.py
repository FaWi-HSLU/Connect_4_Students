from game import Connect4
import platform

class Coordinator_Local:
    """ 
    Coordinator for a local Connect 4 game with two local players.
    """

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players.
        """
        self.game = Connect4()

        if platform.system() == "Windows":
            from player_local import Player_Local
            self.player1 = Player_Local(self.game)
            self.player2 = Player_Local(self.game)
            self.players = [self.player1, self.player2]
        else: 
            from player_raspi_local import Player_Raspi_Local
            from sense_hat import SenseHat

            self.sense = SenseHat()
            self.player1 = Player_Raspi_Local(self.game, sense=self.sense)
            self.player2 = Player_Raspi_Local(self.game, sense=self.sense)
            self.players = [self.player1, self.player2]

    def play(self):
        """ 
        Main function to run the game with two local players.
        
        This method handles player registration, turn management, 
        and checking for a winner until the game concludes.
        """
        # Register both players in the game
        print("Registering players...")
        self.player1.register_in_game()
        self.player2.register_in_game()

        # Main game loop
        print("Starting main game loop...")
        while not self.game.winner and self.game.counter < self.game.board.size:
            for player in self.players:
                if self.game.winner:
                    break

                if player.is_my_turn():
                    player.visualize()
                    player.make_move()
                    print(f"Player {player.id} made a move.")

                    if self.game.winner:
                        player.celebrate_win()
                        if player.restart_game():
                            self.game.new_game()
                        else:
                            break

                    elif self.game.counter == self.game.board.size:
                        print("The game is a draw!")
                        if player.restart_game():
                            self.game.new_game()
                        else:
                            break

if __name__ == "__main__":
    # Create a coordinator and start the game
    coordinator = Coordinator_Local()
    coordinator.play()