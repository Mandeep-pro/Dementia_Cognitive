from flask import Blueprint

from app.models.game_model import get_all_games, get_game_by_id


game_bp = Blueprint("game", __name__)


# ==========================================
# GET ALL GAMES
# ==========================================

@game_bp.route("/", methods=["GET"])
def get_games():

    games = get_all_games()

    return {
        "status": "success",
        "count": len(games),
        "games": games
    }, 200


# ==========================================
# GET GAME BY ID
# ==========================================

@game_bp.route("/<game_id>", methods=["GET"])
def get_game(game_id):

    game = get_game_by_id(game_id)

    if not game:
        return {
            "status": "error",
            "message": "Game not found"
        }, 404

    return {
        "status": "success",
        "game": game
    }, 200