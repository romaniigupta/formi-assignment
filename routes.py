from flask import render_template, jsonify
import logging

logger = logging.getLogger(__name__)

def init_routes(app):
    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')

    @app.route('/chat')
    def chat():
        """Render chatbot interface"""
        return render_template('chatbot.html')

    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        """Handle 500 errors"""
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": "Internal server error occurred"}), 500