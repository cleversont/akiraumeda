# app.py (versão corrigida)
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import json
from datetime import datetime
from admin.routes import admin_bp
from config import WORKS_JSON, ARTIST_JSON
from admin.utils import load_works_direct, load_artist_direct
from flask_mail import Mail, Message

app = Flask(__name__)

# 🔥 CORREÇÃO: Use os.environ.get() diretamente
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key-for-development')

# Configurações
app.config['WORKS_JSON'] = WORKS_JSON
app.config['ARTIST_JSON'] = ARTIST_JSON
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'media')
app.config['ALLOWED_IMAGE_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['ALLOWED_AUDIO_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# 🔥 REMOVA: load_dotenv() - não é necessário no Railway
# load_dotenv()

# Usuário simples
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# 🔥 CORREÇÃO: Use os.environ.get()
users = {
    '1': User(
        '1', 
        os.environ.get('ADMIN_USERNAME', 'admin'),
        os.environ.get('ADMIN_PASSWORD', 'password123')
    )
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# ... resto do código permanece igual ...

@app.route('/debug-env')
def debug_env():
    """Debug detalhado das variáveis de ambiente"""
    debug_info = {
        'ADMIN_USERNAME': os.environ.get('ADMIN_USERNAME'),
        'ADMIN_PASSWORD_SET': bool(os.environ.get('ADMIN_PASSWORD')),
        'SECRET_KEY_SET': bool(os.environ.get('SECRET_KEY')),
        'FLASK_ENV': os.environ.get('FLASK_ENV'),
        'ALL_ENV_VARS': {k: '***' if 'PASSWORD' in k or 'KEY' in k else v 
                        for k, v in os.environ.items() if 'ADMIN' in k or 'SECRET' in k or 'FLASK' in k}
    }
    return debug_info

# No FINAL do app.py, substitua o if __name__ == '__main__' por:

# Esta parte deve ser a ÚLTIMA do arquivo
if __name__ == '__main__':
    # No Railway, use a porta da variável de ambiente
    port = int(os.environ.get('PORT', 5000))
    
    # Debug apenas em desenvolvimento
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(
        host='0.0.0.0',  # Importante para Railway
        port=port,
        debug=debug
    )
