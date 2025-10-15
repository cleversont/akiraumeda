# admin/utils.py
import json
import os
from datetime import datetime
from flask import current_app

def load_works():
    """Carrega os trabalhos do arquivo JSON - PARA USO DENTRO DO CONTEXTO FLASK"""
    try:
        with open(current_app.config['WORKS_JSON'], 'r', encoding='utf-8') as f:
            works = json.load(f)
            
            # CORREÇÃO: Garantir que todas as categorias existem
            categorias_esperadas = ['musica', 'fotografia', 'desenho', 'arte_digital', 'news']
            for categoria in categorias_esperadas:
                if categoria not in works:
                    works[categoria] = []
            
            return works
    except FileNotFoundError:
        # Se o arquivo não existe, cria um novo
        default_data = {
            "musica": [],
            "fotografia": [],
            "desenho": [],
            "arte_digital": [],
            "news": []  # Adicionando news por padrão
        }
        save_works(default_data)
        return default_data

def load_works_direct(path):
    """Carrega os trabalhos do arquivo JSON - PARA USO FORA DO CONTEXTO FLASK"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "musica": [],
            "fotografia": [],
            "desenho": [],
            "arte_digital": []
        }

def save_works(works_data):
    """Salva os trabalhos no arquivo JSON - Versão mais segura"""
    try:
        # Primeiro salvar em um arquivo temporário
        temp_file = current_app.config['WORKS_JSON'] + '.tmp'
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(works_data, f, ensure_ascii=False, indent=2)
        
        # Verificar se o arquivo temporário é JSON válido
        with open(temp_file, 'r', encoding='utf-8') as f:
            json.load(f)  # Isso vai gerar erro se não for válido
        
        # Se chegou aqui, o JSON é válido, então substituir o original
        import os
        os.replace(temp_file, current_app.config['WORKS_JSON'])
        
    except Exception as e:
        # Se algo der errado, remover o arquivo temporário
        try:
            import os
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass
        raise e

def load_artist_direct(path):
    """Carrega os dados do artista - PARA USO FORA DO CONTEXTO FLASK"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "nome": "Nome do Artista",
            "bio": "Breve biografia do artista...",
            "email": "artista@email.com",
            "social_links": {
                "instagram": "https://instagram.com/artista",
                "youtube": "https://youtube.com/artista", 
                "spotify": "https://open.spotify.com/artist/..."
            }
        }
def load_artist():
    """Carrega os dados do artista do arquivo JSON - PARA USO DENTRO DO CONTEXTO FLASK"""
    try:
        with open(current_app.config['ARTIST_JSON'], 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo não existe, retorna dados padrão
        return {
            "nome": "AKIRA UMEDA",
            "bio": "Artista multifacetado",
            "email": "dildlo@gmail.com",
            "social_links": {
                "instagram": "",
                "youtube": "",
                "spotify": "",
                "bandcamp1": "",
                "bandcamp2": ""
            }
        }

def save_artist(artist_data):
    """Salva os dados do artista"""
    with open(current_app.config['ARTIST_JSON'], 'w', encoding='utf-8') as f:
        json.dump(artist_data, f, ensure_ascii=False, indent=2)

def generate_id():
    """Gera um ID único baseado no timestamp"""
    return int(datetime.now().timestamp())

def allowed_file(filename, file_type='image'):
    """Verifica se a extensão do arquivo é permitida"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    elif file_type == 'audio':
        return ext in current_app.config['ALLOWED_AUDIO_EXTENSIONS']
    
    return False
