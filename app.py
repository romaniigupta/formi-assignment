import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SESSION_SECRET", "barbeque-nation-agent-secret")

# Enable CORS
CORS(app)

# Import route modules after app is created
from api.knowledge_base import knowledge_base_bp
from api.post_call_analysis import post_call_bp
from api.conversation_service import conversation_bp

# Register blueprints
app.register_blueprint(knowledge_base_bp, url_prefix='/api/knowledge')
app.register_blueprint(post_call_bp, url_prefix='/api/logs')
app.register_blueprint(conversation_bp, url_prefix='/api/conversation')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
