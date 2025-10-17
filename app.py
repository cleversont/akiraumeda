# app.py
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from datetime import datetime
from admin.routes import admin_bp
from config import WORKS_JSON, ARTIST_JSON
from admin.utils import load_works_direct, load_artist_direct
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'C7C7a4twgw*')  # ← MUDAR AQUI

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

# Carrega variáveis do .env
load_dotenv()

# Usuário simples (agora usando variáveis de ambiente)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Usuário carregado das variáveis de ambiente
users = {
    '1': User(
        '1', 
        os.getenv('ADMIN_USERNAME', 'admin'),  # Valor padrão caso a variável não exista
        os.getenv('ADMIN_PASSWORD', 'password123')  # Valor padrão
    )
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Garantir que os diretórios existem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'imagens'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'musicas'), exist_ok=True)

# Registrar Blueprint do Admin
app.register_blueprint(admin_bp)

# Funções para carregar dados do JSON
def load_works_data():
    return load_works_direct(WORKS_JSON)

def load_artist_data():
    return load_artist_direct(ARTIST_JSON)

# Rotas de Autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_page = request.args.get('next')
        
        print(f"🔐 Tentativa de login: {username}")  # Log no Railway
        
        user = users.get('1')
        
        # Debug detalhado
        print(f"📝 Usuário esperado: {user.username if user else 'NONE'}")
        print(f"🔑 Senha esperada: {'***' if user and user.password else 'NONE'}")
        print(f"📝 Usuário fornecido: {username}")
        print(f"🔑 Senha fornecida: {'***' if password else 'NONE'}")
        
        if user and user.username == username and user.password == password:
            login_user(user)
            print("✅ Login bem-sucedido!")
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            print("❌ Login falhou - credenciais incorretas")
            flash('Usuário ou senha incorretos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))
    
# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Ou seu provedor de email
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # Substitua pelo seu email
app.config['MAIL_PASSWORD'] = 'sua_senha_de_app'     # Substitua pela senha de app
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'

mail = Mail(app)

# Rotas principais (mantidas)
@app.route('/')
def home():
    works = load_works_data()
    artist = load_artist_data()
    return render_template('index.html', artista=artist, portfolio=works, now=datetime.now())

@app.route('/sobre')
def sobre():
    artist = load_artist_data()
    return render_template('sobre.html', artista=artist, now=datetime.now())

from email_utils import send_contact_email

# app.py - Adicione estas rotas

@app.route('/contato')
def contato():
    """Página de contato"""
    return render_template('contato.html')

@app.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    """Processa o formulário de contato"""
    try:
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        
        print(f"📨 Recebido formulário: {nome}, {email}, {mensagem}")  # Debug
        
        # Validação básica
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('index') + '#contato')
        
        # Verificar se o email está configurado
        if not os.getenv('EMAIL_USER') or not os.getenv('EMAIL_PASSWORD'):
            print("⚠️ Email não configurado - salvando mensagem localmente")
            # Salvar em um arquivo de log como fallback
            with open('contact_messages.log', 'a', encoding='utf-8') as f:
                f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M')} ---\n")
                f.write(f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}\n")
            
            flash('Mensagem recebida! Entrarei em contato em breve. (Sistema de email offline)', 'success')
            return redirect(url_for('index') + '#contato')
        
        # Tentar enviar email
        if send_contact_email(nome, email, mensagem):
            flash('Mensagem enviada com sucesso! Entrarei em contato em breve.', 'success')
        else:
            flash('Erro ao enviar mensagem. Por favor, tente novamente ou me contate diretamente por email.', 'error')
        
        # Redireciona de volta para a seção de contato na página inicial
        return redirect(url_for('index') + '#contato')
    
    except Exception as e:
        print(f"❌ Erro crítico no formulário: {e}")
        flash('Erro interno no sistema. Por favor, tente novamente mais tarde.', 'error')
        return redirect(url_for('index') + '#contato')
@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory('static/media', filename)
    
# Adicione esta rota ao app.py (temporariamente)
@app.route('/corrigir-caminhos')
def corrigir_caminhos():
    from admin.utils import load_works, save_works
    works = load_works()
    corrigidos = 0
    
    # Verificar se os arquivos existem e corrigir caminhos
    for categoria in ['musica', 'fotografia', 'desenho', 'arte_digital']:
        for trabalho in works[categoria]:
            # Corrigir áudio
            if 'audio' in trabalho:
                audio_path = trabalho['audio']
                # Se não começa com 'musicas/', adicionar
                if not audio_path.startswith('musicas/'):
                    novo_caminho = f"musicas/{audio_path}"
                    # Verificar se o arquivo existe no novo caminho
                    if os.path.exists(os.path.join('static/media', novo_caminho)):
                        trabalho['audio'] = novo_caminho
                        corrigidos += 1
                        print(f"✅ Áudio corrigido: {audio_path} -> {novo_caminho}")
            
            # Corrigir imagem
            if 'imagem' in trabalho:
                imagem_path = trabalho['imagem']
                # Se não começa com 'imagens/', adicionar
                if not imagem_path.startswith('imagens/'):
                    novo_caminho = f"imagens/{imagem_path}"
                    # Verificar se o arquivo existe no novo caminho
                    if os.path.exists(os.path.join('static/media', novo_caminho)):
                        trabalho['imagem'] = novo_caminho
                        corrigidos += 1
                        print(f"✅ Imagem corrigida: {imagem_path} -> {novo_caminho}")
    
    save_works(works)
    return f'Caminhos corrigidos: {corrigidos}. Recarregue a página principal para ver as mudanças.'

# Adicione esta rota ao app.py
@app.route('/debug-works')
def debug_works():
    works = load_works_data()
    return {
        'works': works,
        'works_file': WORKS_JSON,
        'file_exists': os.path.exists(WORKS_JSON)
    }

def init_data_files():
    """Inicializa os arquivos JSON se não existirem"""
    import json
    import os
    from config import DATA_DIR, WORKS_JSON, ARTIST_JSON
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Criar pastas de upload
    upload_dirs = [
        'static/media/imagens',
        'static/media/musicas',
        'static/media/temp'
    ]
    
    for dir_path in upload_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Pasta criada/verificada: {dir_path}")
    
    if not os.path.exists(WORKS_JSON):
        default_works = {"musica": [], "fotografia": [], "desenho": [], "arte_digital": []}
        with open(WORKS_JSON, 'w', encoding='utf-8') as f:
            json.dump(default_works, f, ensure_ascii=False, indent=2)
       # print(f"✅ Arquivo {WORKS_JSON} criado com sucesso!")
    
    if not os.path.exists(ARTIST_JSON):
        default_artist = {
            "nome": "Nome do Artista",
            "bio": "Breve biografia do artista...",
            "email": "artista@email.com",
            "social_links": {
                "instagram": "https://instagram.com/artista",
                "youtube": "https://youtube.com/artista", 
                "spotify": "https://open.spotify.com/artist/...",
                "bandcamp1": "",
                "bandcamp2": ""
            }
        }
        with open(ARTIST_JSON, 'w', encoding='utf-8') as f:
            json.dump(default_artist, f, ensure_ascii=False, indent=2)
       # print(f"✅ Arquivo {ARTIST_JSON} criado com sucesso!")
        
def allowed_file(filename, file_type='image'):
    """Verifica se a extensão do arquivo é permitida"""
    if '.' not in filename:
        print(f"❌ Arquivo sem extensão: {filename}")  # DEBUG
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    print(f"🔍 Verificando extensão: {ext} para tipo: {file_type}")  # DEBUG
    
    if file_type == 'image':
        allowed = ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
        print(f"🖼️ Extensão {ext} permitida para imagem: {allowed}")  # DEBUG
        return allowed
    elif file_type == 'audio':
        allowed = ext in current_app.config['ALLOWED_AUDIO_EXTENSIONS']
        print(f"🎵 Extensão {ext} permitida para áudio: {allowed}")  # DEBUG
        return allowed
    
    return False

@app.route('/testar-email')
def testar_email():
    """Rota temporária para testar o email"""
    if send_contact_email("Teste", "teste@exemplo.com", "Esta é uma mensagem de teste"):
        return "✅ Email enviado com sucesso!"
    else:
        return "❌ Falha no envio de email"
        
@app.route('/sitemap.xml')
def sitemap():
    """Gera sitemap.xml dinâmico para SEO"""
    try:
        from flask import render_template_string
        base_url = request.url_root.rstrip('/')
        
        # URLs do site com prioridades
        pages = [
            {'loc': '', 'priority': '1.0', 'changefreq': 'weekly'},
            {'loc': '/#musica', 'priority': '0.9', 'changefreq': 'monthly'},
            {'loc': '/#fotografia', 'priority': '0.9', 'changefreq': 'monthly'},
            {'loc': '/#desenho', 'priority': '0.9', 'changefreq': 'monthly'},
            {'loc': '/#arte_digital', 'priority': '0.9', 'changefreq': 'monthly'},
            {'loc': '/#news', 'priority': '0.8', 'changefreq': 'weekly'},
            {'loc': '/#contato', 'priority': '0.7', 'changefreq': 'monthly'},
        ]
        
        sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{% for page in pages %}
    <url>
        <loc>{{ base_url }}{{ page.loc }}</loc>
        <priority>{{ page.priority }}</priority>
        <changefreq>{{ page.changefreq }}</changefreq>
        <lastmod>{{ now.strftime('%Y-%m-%d') }}</lastmod>
    </url>
{% endfor %}
</urlset>'''
        
        return render_template_string(
            sitemap_xml, 
            pages=pages, 
            base_url=base_url,
            now=datetime.now()
        ), 200, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        return f"Erro ao gerar sitemap: {e}", 500
        
        return render_template_string(sitemap_xml, base_url=base_url, pages=pages), 200, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        return f"Erro ao gerar sitemap: {e}", 500
        
@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve arquivos estáticos com cache"""
    response = send_from_directory('static', filename)
    response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 ano
    return response

@app.route('/debug-auth')
def debug_auth():
    """Debug das credenciais de autenticação"""
    import os
    user = users.get('1')
    
    debug_info = {
        'ADMIN_USERNAME_env': os.environ.get('ADMIN_USERNAME'),
        'ADMIN_PASSWORD_env': '***' if os.environ.get('ADMIN_PASSWORD') else 'NÃO CONFIGURADO',
        'user_username': user.username if user else 'NÃO ENCONTRADO',
        'user_password': '***' if user and user.password else 'NÃO CONFIGURADO',
        'users_dict': {k: vars(v) for k, v in users.items()} if users else 'VAZIO'
    }
    
    return f"""
    <h1>Debug Autenticação</h1>
    <pre>{json.dumps(debug_info, indent=2)}</pre>
    <p><a href="/admin">Tentar admin</a></p>
    """

# Configurações para produção
if __name__ == '__main__':
    # Obter porta do ambiente (para produção) ou usar 5000 localmente
    port = int(os.environ.get('PORT', 5000))
    
    # Verificar se está em produção
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(
        host='0.0.0.0',  # Importante para aceitar conexões externas
        port=port, 
        debug=debug_mode  # Debug desligado em produção
    )
    
