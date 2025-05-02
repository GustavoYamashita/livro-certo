//  Modal Script
const openButtons = document.querySelectorAll('.open-modal');

openButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modalID = button.getAttribute('data-modal');
        const modal = document.getElementById(modalID);

        modal.showModal();
    });
});

const closeButtons = document.querySelectorAll('.close-modal');

closeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modalID = button.getAttribute('data-modal'); 
        const modal = document.getElementById(modalID);
        
        modal.close();
    });
});

window.addEventListener("click", (event) => {
    const modals = document.querySelectorAll('dialog');

    modals.forEach(modal => {
        // Fecha apenas se o clique for diretamente no <dialog>, e não no conteúdo interno
        if (event.target === modal) {
            modal.close();
        }
    });
});

// Sistema de busca biblioteca
document.addEventListener('DOMContentLoaded', function() {
    const campoBusca = document.querySelector('.campo-busca');
    const botaoFiltrar = document.querySelector('.botao-filtrar');
    
    botaoFiltrar.addEventListener('click', function() {
        const termo = campoBusca.value.trim();
        if(termo) {
            window.location.href = `?busca=${encodeURIComponent(termo)}`;
        }
    });
    
    campoBusca.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            botaoFiltrar.click();
        }
    });
});

