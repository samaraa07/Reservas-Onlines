document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        // 1. Evento principal de clique no botão hambúrguer
        navToggle.addEventListener('click', function() {
            // Alterna a classe 'active' para abrir/fechar o menu
            navLinks.classList.toggle('active');
            // Alterna a classe 'active' para transformar o ícone em 'X'
            navToggle.classList.toggle('active'); 
        });
        
        // 2. Fechar o menu ao clicar em qualquer link (Melhora a experiência do usuário)
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                // Remove as classes 'active' para fechar o menu
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }
});