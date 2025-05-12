import os
import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import Config
from models import db
from routes import init_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SESSION_SECRET", "barbeque-nation-agent-secret")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Check if DATABASE_URL is set
if not app.config['SQLALCHEMY_DATABASE_URI']:
    logger.warning("DATABASE_URL not set. Using SQLite for development.")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbeque_nation.db'

# Initialize extensions
db.init_app(app)
CORS(app)

# Import route modules after app is created
from api.knowledge_base import knowledge_base_bp
from api.post_call_analysis import post_call_bp
from api.conversation_service import conversation_bp

# Register blueprints
app.register_blueprint(knowledge_base_bp, url_prefix='/api/knowledge')
app.register_blueprint(post_call_bp, url_prefix='/api/logs')
app.register_blueprint(conversation_bp, url_prefix='/api/conversation')

# Initialize routes
init_routes(app)

# Create database tables
with app.app_context():
    logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.create_all()
    logger.info("Database tables created successfully")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
