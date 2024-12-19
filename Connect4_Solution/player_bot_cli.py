from player_remote import Player_Remote

from Bot.chatgpt_bot import Connect4Bot


class Bot_Remote(Player_Remote):


    def __init__(self, **kwargs) -> None:
        """
        Initialize the a BOT player to play with the provided API URL.

        Parameters:
            api_url (str): The base URL of the Connect 4 API server (e.g., http://localhost:5000).
        
        Raises:
            ValueError: If 'api_url' is not provided in kwargs.
        """
        super().__init__(**kwargs)

        self.bot = Connect4Bot()

    
    def make_move(self) -> bool:
        """ 
        Make a move using the ChatGPT Bot
        """
        try:
            
            move_made = False
            while not move_made:
                
                board = self.get_board()
                print(f"Asking ChatGPT for next move")
                col = self.bot.make_move(board=board, active_icon=self.icon)
                print(f"ChatGPT chose column {col}")

                move_made = super().make_move(col)
            
            return True
        except:
            return False
        
    
    def register_in_game(self):
        super().register_in_game()

        print(f"Bot has Icon {self.icon}")
         