from abc import ABC, abstractmethod
import uuid

class Player(ABC):
    """
    Abstract Base Player class to define common methods for both Local and Remote players.

    Attributes:
        id (UUID): Unique identifier for the player.
        icon ('X' or 'O'): The player's icon used in the game. (set during registration)
        board_width (int):  Number of Horizontal Elements (set to 8)
        board_height (int): Number of Vertical Elements (set to 7)
    """

    def __init__(self) -> None:
        self.id = uuid.uuid4()          # Assign a unique ID to the player
        self.icon:str = None            # Icon will be set later during player registration

        self.board_width:int = 8        # Set the width of the board
        self.board_height:int = 7       # Set the height of the board
        
    @abstractmethod
    def register_in_game(self) -> str:
        """
        Register the player in the game and assign an icon.
        
        Returns:
            str: The player's icon.
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'register_in_game'")

    @abstractmethod
    def is_my_turn(self) -> bool:
        """
        Check if it's the player's turn.
        
        Returns:
            bool: True if it's the player's turn, False otherwise.
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'is_my_turn'")

    @abstractmethod
    def get_game_status(self) -> tuple[str,str,bool,int]:
        """
        Get the current game status.
        
        Returns:
            tuple: A tuple containing (active_icon, active_player, winner, turn_number).
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'get_game_status'")

    @abstractmethod
    def make_move(self) -> bool:
        """
        Prompt the player to make a move.
        
        Returns:
            bool: True if the move was successful, False otherwise.
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'make_move'")

    @abstractmethod
    def visualize(self)->None:
        """
        Visualize the current board state

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'visualize'")
    
    @abstractmethod
    def celebrate_win(self)->None:
        """
        Players personal "celebration" on how to visualize a Win

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'celebrate_win'")