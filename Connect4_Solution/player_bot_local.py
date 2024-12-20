from player_local import Player_Local

from Bot.chatgpt_bot import Connect4Bot


class Bot_Local(Player_Local):

    def __init__(self, **kwargs) -> None:
        """
        Initialize the a BOT player to play with the provided API URL.

        Parameters:
            game: (Connect4)        Connect4 instance
        
        Raises:
            ValueError: If 'game' is not provided in kwargs.
        """
        super().__init__(**kwargs)

        self.bot = Connect4Bot()

    
    def make_move(self) -> int:
        """ 
        Make a move using the ChatGPT Bot
        """
        tries = 1
        while True:
            try:
                board = self.game.get_board()
                col = self.bot.make_move(board=board, active_icon=self.icon)
                return col
            except:
                tries+= 1
                print(f"Error while Prompting ChatGPT ... trying again (Try {tries})")
                