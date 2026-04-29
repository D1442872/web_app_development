from flask import Blueprint

# 將各個模組的 blueprint 引入
from .events import events_bp
from .user import user_bp
from .admin import admin_bp

def init_app(app):
    """
    註冊所有的 blueprints 到主要的 app 實例中
    """
    app.register_blueprint(events_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
