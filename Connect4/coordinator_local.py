from game import Connect4
from player_local import Player_Local


class Coordinator_Local:
    """ 
    Coordinator for a local Connect 4 game with two local players.
    """

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players.
        """
        self.game = Connect4()
        self.player1 = Player_Local(self.game)
        self.player2 = Player_Local(self.game)
        self.players = [self.player1, self.player2]

    def play(self):
        """ 
        Main function to run the game with two local players.
        
        This method handles player registration, turn management, 
        and checking for a winner until the game concludes.
        """
        # Register both players in the game
        self.player1.register_in_game()
        self.player2.register_in_game()

        # Main game loop
        while not self.game.winner and self.game.counter < self.game.board.size:
            for player in self.players:
                if self.game.winner:
                    break

                if player.is_my_turn():
                    player.visualize()
                    move = player.make_move()

                    if self.game.winner:
                        player.celebrate_win()
                        break

        if not self.game.winner:
            print("The game is a draw!")

if __name__ == "__main__":
    # Create a coordinator and start the game
    coordinator = Coordinator_Local()
    coordinator.play()
