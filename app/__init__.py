from flask import Flask
import os
import sqlite3

def init_db():
    from app.models.db_models import DATABASE_PATH
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    from .routes.events import events_bp
    from .routes.user import user_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(events_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
