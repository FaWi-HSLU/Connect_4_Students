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
            active_icon, active_id, winner, turn_number = self.game.get_status()
            return jsonify({
                'active_icon': active_icon,
                'active_id': str(active_id) if active_id else None,
                'winner': winner,
                'turn_number':turn_number
            })

        # 2. Expose register_player method
        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            try:
                player_id = uuid.UUID(request.json['player_id'])
            except (KeyError, ValueError):
                return jsonify({"error": "Invalid player ID"}), 400

            icon = self.game.register_player(player_id)
            
            if icon is None:
                return jsonify({"error": "Game is full or player already registered"}), 400

            return jsonify({'player_icon': icon})


        # 3. Expose get_board method
        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            """
            Return the Board as a List of Strings
                
            Returns:
                dict    'board': list of len 56
            """
            board = self.game.get_board()
            board_list = board.tolist()  # Convert numpy array to a list for JSON serialization
            return jsonify({'board': board_list})

        # 4. Expose move method
        @self.app.route('/connect4/check_move', methods=['POST'])
        def check_move():
            try:
                column = int(request.json['column'])
                player_id = uuid.UUID(request.json['player_id'])
            except (KeyError, ValueError):
                return jsonify({"error": "Invalid input"}), 400

            result = self.game.check_move(column, player_id)
            if not result:
                return jsonify({"error": "Illegal move"}), 400

            return jsonify({'success': True})

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