from flask import Flask
from flask_cors import CORS

from app.routes.auth_routes import auth_bp
from app.routes.patient_routes import patient_bp
from app.routes.game_routes import game_bp

from app.routes.game_result_routes import game_result_bp

from app.routes.reminder_routes import reminder_bp

from app.routes.memory_routes import memory_bp

from app.routes.caregiver_routes import caregiver_bp

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        patient_bp,
        url_prefix="/api/patients"
    )

    app.register_blueprint(
        game_bp,
        url_prefix="/api/games"
    )

    app.register_blueprint(
    game_result_bp,
    url_prefix="/api/game-results"
)

    app.register_blueprint(
    reminder_bp,
    url_prefix="/api/reminders"
)
    
    app.register_blueprint(
    memory_bp,
    url_prefix="/api/memories"
)

    app.register_blueprint(
    caregiver_bp,
    url_prefix="/api/caregiver"
)
    

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {
            "status": "success",
            "message": "SmritiRoots backend is running"
        }, 200

    return app