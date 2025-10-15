# admin/__init__.py
from .utils import load_works as load_works_data, load_artist as load_artist_data

# Estas funções serão usadas fora do contexto da aplicação
def init_data():
    """Inicializa os dados JSON se não existirem"""
    from config import WORKS_JSON, ARTIST_JSON
    import json
    import os
    
    # Criar works.json se não existir
    if not os.path.exists(WORKS_JSON):
        default_works = {
            "musica": [],
            "fotografia": [],
            "desenho": [],
            "arte_digital": []
        }
        with open(WORKS_JSON, 'w', encoding='utf-8') as f:
            json.dump(default_works, f, ensure_ascii=False, indent=2)
    
    # Criar artist.json se não existir
    if not os.path.exists(ARTIST_JSON):
        default_artist = {
            "nome": "Nome do Artista",
            "bio": "Breve biografia do artista...",
            "email": "artista@email.com",
            "social_links": {
                "instagram": "https://instagram.com/artista",
                "youtube": "https://youtube.com/artista",
                "spotify": "https://open.spotify.com/artist/..."
            }
        }
        with open(ARTIST_JSON, 'w', encoding='utf-8') as f:
            json.dump(default_artist, f, ensure_ascii=False, indent=2)
