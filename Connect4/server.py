import uuid

import socket                                               # to get own IP
from flask import Flask, request, jsonify                   # for api
from flask_swagger_ui import get_swaggerui_blueprint        # for swagger documentation


# local includes
from game import Connect4


class Connect4Server:
    """
    Game Server
        Runs on Localhost
    
    Attributes
        game (Connect4):    Local Instance of Connect4 Game (with all game rules)
        app (Flask):        Web Server Instance

    """
    def __init__(self):
        """
        Create a Connect4 Server on localhost (127.0.0.1)
        - Add SWAGGER UI Documentation
        - Expose API Methods
        """

        self.game = Connect4()  # Connect4 game instance
        self.app = Flask(__name__)  # Flask app instance

        # Swagger UI Configuration
        SWAGGER_URL = '/swagger/connect4/'
        API_URL = '/static/swagger.json'  # This should point to your static swagger.json file
        
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Connect 4 API",
                'layout': "BaseLayout"  # You can choose other layouts
            }
        )

        # Register the Swagger UI blueprint
        self.app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


        # Define API routes within the constructor
        self.setup_routes()

    def setup_routes(self):
        """
        Expose the following Methods
        """
        # Overall Description
        @self.app.route('/')
        def index():
            return "Welcome to the Connect 4 API!"



        # 1. Expose get_status method
        @self.app.route('/connect4/status', methods=['GET'])
        def get_status():
            # Call the get_status method from the Connect4 instance (returns a dictionnary)
            status = self.game.get_status()
            # Return the status as a JSON response
            return jsonify(status)


        # 2. Expose register_player method
        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            # Generate a unique player ID
            player_id = uuid.uuid4()
            # Call the register_player method from the Connect4 instance
            icon = self.game.register_player(player_id)
            # Return the player ID and icon as a JSON response
            return jsonify({"player_id": str(player_id), "icon": icon})


        # 3. Expose get_board method
        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            # Call the get_board method from the Connect4 instance
            board = self.game.get_board()
            # Convert the NumPy array to a list
            board_list = board.tolist()
            # Return the board as a JSON response
            return jsonify(board_list)

        # 4. Expose move method
        @self.app.route('/connect4/make_move', methods=['POST'])
        def make_move():
            data = request.get_json()
            player_id = data.get('player_id')
            column = data.get('column')

            # Validate input
            if not player_id or not column:
                return jsonify({"error": "Invalid input: player_id and column are required"}), 400

            try:
                player_id = uuid.UUID(player_id)
                column = int(column)
            except ValueError:
                return jsonify({"error": "Invalid input format: player_id must be a valid UUID and column must be an integer"}), 400

            # Check if the player is registered
            if player_id not in self.game.registered.values():
                return jsonify({"error": "Player not registered"}), 400

            # Make the move
            move_valid = self.game.check_move(column, player_id)
            if move_valid:
                status = self.game.get_status()
                return jsonify({
                    "success": True,
                    "board": self.game.get_board().tolist(),
                    "status": status
                })
            else:
                return jsonify({"error": "Invalid move: column is full or out of bounds"}), 400


    def run(self, debug=True, host='0.0.0.0', port=5000):
        # Get and display the local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Server is running on {local_ip}:{port}")

        # Start the Flask app
        self.app.run(debug=debug, host=host, port=port)



# If you want to run the server directly:
if __name__ == '__main__':
    server = Connect4Server()  # Initialize the Connect4Server
    server.run()               # Start the Flask app