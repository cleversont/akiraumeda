document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const categorias = document.querySelectorAll('.categoria');
    const mainContent = document.querySelector('.main-content');
    
    // Estado inicial - página em branco
    let currentSection = null;
    
    // Mostrar seção específica
    function showSection(sectionId) {
        // Esconde todas as seções
        categorias.forEach(categoria => {
            categoria.classList.remove('active');
        });
        
        // Remove active de todos os links
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Mostra a seção clicada
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            currentSection = sectionId;
            
            // Scroll para o topo da seção
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
        
        // Ativa o link correspondente
        const activeLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
    
    // Event listeners para os links de navegação
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            showSection(targetId);
            
            // Atualiza a URL
            history.pushState(null, null, `#${targetId}`);
        });
    });
    
    // Verificar hash na URL ao carregar
    function checkInitialHash() {
        const hash = window.location.hash.substring(1);
        if (hash && document.getElementById(hash)) {
            showSection(hash);
        }
        // Se não houver hash, a página fica em branco
    }
    
    // Verificar quando o usuário navega com botões voltar/avancar
    window.addEventListener('popstate', checkInitialHash);
    
    // Inicializar
    checkInitialHash();
    
    // Lightbox para imagens
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const closeBtn = document.querySelector('.lightbox .close');
    
    if (lightbox) {
        document.querySelectorAll('.photo-card, .art-card').forEach(card => {
            card.addEventListener('click', function() {
                const img = this.querySelector('img');
                const title = this.querySelector('h4')?.textContent || '';
                
                if (img) {
                    lightboxImg.src = img.src;
                    lightboxTitle.textContent = title;
                    lightbox.style.display = 'block';
                    document.body.style.overflow = 'hidden';
                }
            });
        });
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }
        
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }
});

// Adicione esta função para expandir/recolher notícias
function toggleNewsContent(button) {
    const newsCard = button.closest('.news-card');
    const fullContent = newsCard.querySelector('.news-full-content');
    const excerpt = newsCard.querySelector('.news-excerpt');
    
    if (fullContent.style.display === 'none') {
        fullContent.style.display = 'block';
        if (excerpt) excerpt.style.display = 'none';
        button.textContent = 'Ler menos';
    } else {
        fullContent.style.display = 'none';
        if (excerpt) excerpt.style.display = 'block';
        button.textContent = 'Ler mais';
    }
}

// Adicione também ao menu de navegação
// (O JavaScript existente já deve lidar com a navegação)
