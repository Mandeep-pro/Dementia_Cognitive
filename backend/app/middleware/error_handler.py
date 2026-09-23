from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "message": getattr(error, "description", "Bad request")
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "status": "error",
            "message": getattr(error, "description", "Unauthorized")
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "status": "error",
            "message": getattr(error, "description", "Forbidden")
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": getattr(error, "description", "Resource not found")
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
