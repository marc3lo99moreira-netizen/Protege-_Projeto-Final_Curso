// --- FUNCTION PARA FAZER LOGOUT (LIMPAR FILTROS) ---
function fazerLogout(logoutUrl) {
    // Limpar localStorage
    localStorage.removeItem('modoDaltonismo');
    localStorage.removeItem('modoContraste');
    
    // Remover classes CSS do body
    document.body.classList.remove('protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia');
    document.body.classList.remove('alto-contraste', 'contraste-invertido', 'modo-escuro');
    
    console.log('✓ Filtros limpos. Redirecionando...');
    
    // Se não passar URL, usar a padrão
    if (!logoutUrl) {
        logoutUrl = '/logout/';
    }
    
    // Redirecionar para logout (após um pequeno delay para garantir que tudo está limpo)
    setTimeout(() => {
        window.location.href = logoutUrl;
    }, 100);
}
// --- FUNÇÃO DO MENU DE PERFIL ---
function PerfilMenu() {
    const menu = document.getElementById('perfil-menu');
    if (menu) {
        // Fecha os outros menus de acessibilidade para não sobrepor
        document.getElementById('daltonismo-menu')?.classList.add('hidden');
        document.getElementById('contraste-menu')?.classList.add('hidden');
        console.log('PerfilMenu() called — menu before toggle:', menu.classList.contains('hidden'));
        menu.classList.toggle('hidden');
        console.log('PerfilMenu() after toggle — hidden:', menu.classList.contains('hidden'));
    }
}

// --- GESTÃO GLOBAL DE CLIQUES (FECHAR MENUS) ---
// --- GESTÃO GLOBAL DE CLIQUES (FECHAR MENUS) ---
window.addEventListener('click', function(e) {
    const daltMenu = document.getElementById('daltonismo-menu');
    const contMenu = document.getElementById('contraste-menu');
    const perfMenu = document.getElementById('perfil-menu');
    
    // Se o clique foi DENTRO da área de perfil (botão ou menu), não fecha nada do perfil
    if (e.target.closest('.profile-area')) {
        return; 
    }

    // Se o clique foi DENTRO da área de acessibilidade, não fecha acessibilidade
    if (e.target.closest('.accessibility-pill') || e.target.closest('.accessibility-menu')) {
        return;
    }

    // Se clicou fora de tudo, fecha todos os menus abertos
    if (perfMenu) perfMenu.classList.add('hidden');
    if (daltMenu) daltMenu.classList.add('hidden');
    if (contMenu) contMenu.classList.add('hidden');
});

// --- FUNÇÕES DE CONTROLO DE MENUS ACESSIBILIDADE ---
function toggleDaltonismoMenu() {
    document.getElementById('perfil-menu')?.classList.add('hidden');
    document.getElementById('contraste-menu')?.classList.add('hidden');
    const menu = document.getElementById('daltonismo-menu');
    menu.classList.toggle('hidden');
}

function toggleContrasteMenu() {
    document.getElementById('perfil-menu')?.classList.add('hidden');
    document.getElementById('daltonismo-menu')?.classList.add('hidden');
    const menu = document.getElementById('contraste-menu');
    menu.classList.toggle('hidden');
}

// --- FUNÇÃO PARA GUARDAR FILTRO NO SERVIDOR ---
function guardarFiltroNoServidor(tipo, valor) {
    console.log(`Guardando filtro: ${tipo} = ${valor}`);
    
    fetch('/atividades/api/atualizar-filtros/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            tipo: tipo,
            valor: valor
        })
    })
    .then(response => {
        console.log(`Response status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('Resposta do servidor:', data);
        if (data.status === 'sucesso') {
            console.log('✓ ' + data.mensagem);
        } else {
            console.error('✗ Erro ao guardar filtro:', data.mensagem);
        }
    })
    .catch(error => {
        console.error('✗ Erro na requisição:', error);
    });
}

// --- FUNÇÃO PARA OBTER CSRF TOKEN ---
function getCookie(name) {
    // Primeiro tenta obter do input hidden por name
    let input = document.querySelector(`input[name="${name}"]`);
    if (input && input.value) {
        return input.value;
    }
    
    // Tenta variações comuns do nome
    if (name === 'csrftoken') {
        input = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (input && input.value) {
            return input.value;
        }
    }
    
    // Se não encontrar no input, tenta a cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- FUNÇÕES DE APLICAÇÃO DE FILTROS ---
function setDaltonismo(tipo) {
    document.body.classList.remove('protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia');
    if (tipo !== 'normal') document.body.classList.add(tipo);
    
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, guardar no servidor/BD
    // Se não está, guardar no localStorage 
    if (isAuthenticated) {
        guardarFiltroNoServidor('daltonismo', tipo);
    } else {
        localStorage.setItem('modoDaltonismo', tipo);
    }
    
    document.getElementById('daltonismo-menu').classList.add('hidden');
}

function setContraste(tipo) {
    document.body.classList.remove('alto-contraste', 'contraste-invertido', 'modo-escuro');
    if (tipo !== 'normal') document.body.classList.add(tipo);
    
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, guardar no servidor/BD
    // Se não está, guardar no localStorage
    if (isAuthenticated) {
        guardarFiltroNoServidor('contraste', tipo);
    } else {
        localStorage.setItem('modoContraste', tipo);
    }
    
    document.getElementById('contraste-menu').classList.add('hidden');
}

// --- INICIALIZAÇÃO ---
document.addEventListener('DOMContentLoaded', () => {
    // Verificar se o utilizador está autenticado
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, os filtros já foram injectados pelo Django via classes CSS
    // Não aplicar localStorage, pois pode ter valores de outro utilizador
    if (isAuthenticated) {
        // Limpar localStorage para não interferer com o próximo utilizador
        localStorage.removeItem('modoDaltonismo');
        localStorage.removeItem('modoContraste');
    } else {
        // Utilizador não autenticado: aplicar filtros do localStorage como fallback
        const daltSalvo = localStorage.getItem('modoDaltonismo');
        if (daltSalvo && daltSalvo !== 'normal') {
            document.body.classList.add(daltSalvo);
        }
        
        const contSalvo = localStorage.getItem('modoContraste');
        if (contSalvo && contSalvo !== 'normal') {
            document.body.classList.add(contSalvo);
        }
    }

    // Lógica Phishing
    document.querySelectorAll('.phishing-trigger').forEach(el => {
        el.addEventListener('click', () => {
            const info = el.getAttribute('data-info');
            const box = document.getElementById('info-box');
            const text = document.getElementById('info-text');
            if (box && text) {
                text.innerText = info;
                box.classList.remove('hidden');
                setTimeout(() => box.classList.add('hidden'), 5000);
            }
        });
    });

    // Ligar o botão de avatar via event listener (mais robusto que onclick inline)
    const avatarBtn = document.getElementById('btn-avatar-trigger');
    if (avatarBtn) {
        console.log('avatarBtn found, attaching listener');
        avatarBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log('avatarBtn clicked');
            PerfilMenu();
        });
    } else {
        console.log('avatarBtn NOT found on DOMContentLoaded');
    }
});