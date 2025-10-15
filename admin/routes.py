from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from .utils import load_works, save_works, load_artist, save_artist, generate_id, allowed_file

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    """Painel principal do admin"""
    works = load_works()
    artist = load_artist()
    
    # Estatísticas (incluindo news)
    stats = {
        'total_trabalhos': sum(len(works[cat]) for cat in works),
        'musica': len(works['musica']),
        'fotografia': len(works['fotografia']),
        'desenho': len(works['desenho']),
        'arte_digital': len(works['arte_digital']),
        'news': len(works.get('news', []))
    }
    
    return render_template('admin/dashboard.html', 
                         works=works, 
                         artist=artist, 
                         stats=stats,
                         now=datetime.now())

@admin_bp.route('/add-work', methods=['GET', 'POST'])
@login_required
def add_work():
    """Adicionar novo trabalho"""
    artist = load_artist()
    
    if request.method == 'POST':
        categoria = request.form['categoria']
        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '')
        ano = request.form.get('ano', '')
        
        # Campos específicos por categoria
        campos_especificos = {}
        if categoria == 'musica':
            campos_especificos['genero'] = request.form.get('genero', '')
        elif categoria == 'fotografia':
            campos_especificos['categoria_foto'] = request.form.get('categoria_foto', '')
        elif categoria == 'desenho':
            campos_especificos['tecnica'] = request.form.get('tecnica', '')
        elif categoria == 'arte_digital':
            campos_especificos['software'] = request.form.get('software', '')
        elif categoria == 'news':
            campos_especificos['resumo'] = request.form.get('resumo', '')
            campos_especificos['conteudo'] = request.form.get('conteudo', '')
        
        # Processar upload de arquivo
        arquivo = request.files.get('arquivo')
        filename = None
        
        if arquivo and arquivo.filename:
            if categoria == 'musica':
                if allowed_file(arquivo.filename, 'audio'):
                    filename = secure_filename(arquivo.filename)
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'musicas', filename)
                    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                    arquivo.save(upload_path)
                else:
                    flash('Tipo de arquivo de áudio não permitido!', 'error')
                    return redirect(request.url)
            else:
                if allowed_file(arquivo.filename, 'image'):
                    filename = secure_filename(arquivo.filename)
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'imagens', filename)
                    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                    arquivo.save(upload_path)
                else:
                    flash('Tipo de arquivo de imagem não permitido!', 'error')
                    return redirect(request.url)
        
        # Criar novo trabalho
        novo_trabalho = {
            'id': generate_id(),
            'titulo': titulo,
            'descricao': descricao,
            'ano': ano,
            'data_publicacao': datetime.now().strftime('%Y-%m-%d %H:%M'),
            **campos_especificos
        }
        
        # Adicionar nome do arquivo
        if categoria == 'musica' and filename:
            novo_trabalho['audio'] = f"musicas/{filename}"
        elif filename:
            novo_trabalho['imagem'] = f"imagens/{filename}"
        
        # Salvar no JSON - COM CORREÇÃO
        works = load_works()
        
        # CORREÇÃO: Garantir que a categoria existe
        if categoria not in works:
            works[categoria] = []
        
        works[categoria].append(novo_trabalho)
        save_works(works)
        
        flash('Trabalho adicionado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_work.html', 
                          artist=artist, 
                          now=datetime.now())

@admin_bp.route('/edit-artist', methods=['GET', 'POST'])
@login_required
def edit_artist():
    """Editar informações do artista"""
    artist = load_artist()
    
    if request.method == 'POST':
        artist_data = {
            'nome': request.form['nome'],
            'bio': request.form['bio'],
            'email': request.form['email'],
            'social_links': {
                'instagram': request.form.get('instagram', ''),
                'youtube': request.form.get('youtube', ''),
                'spotify': request.form.get('spotify', ''),
                'bandcamp1': request.form.get('bandcamp1', ''),
                'bandcamp2': request.form.get('bandcamp2', '')
            }
        }
        
        save_artist(artist_data)
        flash('Informações do artista atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_artist.html', 
                          artist=artist,
                          now=datetime.now())

@admin_bp.route('/delete-work/<categoria>/<int:work_id>')
@login_required
def delete_work(categoria, work_id):
    """Excluir trabalho"""
    works = load_works()
    
    # Encontrar e remover o trabalho
    works[categoria] = [work for work in works[categoria] if work['id'] != work_id]
    
    save_works(works)
    flash('Trabalho excluído com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/manage-works')
@login_required
def manage_works():
    """Gerenciar todos os trabalhos"""
    works = load_works()
    artist = load_artist()
    return render_template('admin/manage_works.html', 
                          works=works, 
                          artist=artist,
                          now=datetime.now())
