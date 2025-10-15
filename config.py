import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configurações do JSON
DATA_DIR = os.path.join(BASE_DIR, 'data')
WORKS_JSON = os.path.join(DATA_DIR, 'works.json')
ARTIST_JSON = os.path.join(DATA_DIR, 'artist.json')

# Configurações de upload
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'media')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Garantir que os diretórios existem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'imagens'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'musicas'), exist_ok=True)
