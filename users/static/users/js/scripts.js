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
    
    // Redirecionar para logout
    window.location.href = logoutUrl;
}

// --- FUNÇÕES DE AUXÍLIO (CSRF TOKEN) ---
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

// Função para enviar as escolhas para o MySQL (Django)
function salvarPreferenciaNoBanco(tipo, valor) {
    const formData = new FormData();
    formData.append('tipo', tipo);
    formData.append('valor', valor);

    fetch('/users/salvar-acessibilidade/', { // Esta URL deve estar no teu users/urls.py
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) console.error("Erro ao salvar preferência no banco.");
    });
}

// --- FUNÇÕES DE CONTROLO DE MENUS ---
function toggleDaltonismoMenu() {
    document.getElementById('contraste-menu').classList.add('hidden');
    const menu = document.getElementById('daltonismo-menu');
    if (menu) menu.classList.toggle('hidden');
}

function toggleContrasteMenu() {
    document.getElementById('daltonismo-menu').classList.add('hidden');
    const menu = document.getElementById('contraste-menu');
    if (menu) menu.classList.toggle('hidden');
}

function PerfilMenu() {
    document.getElementById('contraste-menu').classList.add('hidden');
    document.getElementById('daltonismo-menu').classList.add('hidden');
    const menu = document.getElementById('perfil-menu');
    if (menu) menu.classList.toggle('hidden');
}

// --- FUNÇÕES DE APLICAÇÃO DE FILTROS ---
function setDaltonismo(tipo) {
    document.body.classList.remove('protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia');
    if (tipo !== 'normal') {
        document.body.classList.add(tipo);
    }
    
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, guardar no servidor/BD
    // Se não está, guardar no localStorage
    if (isAuthenticated) {
        salvarPreferenciaNoBanco('daltonismo', tipo);
    } else {
        localStorage.setItem('modoDaltonismo', tipo);
    }
    
    document.getElementById('daltonismo-menu').classList.add('hidden');
}

function setContraste(tipo) {
    document.body.classList.remove('alto-contraste', 'contraste-invertido', 'modo-escuro');
    if (tipo !== 'normal') {
        document.body.classList.add(tipo);
    }
    
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, guardar no servidor/BD
    // Se não está, guardar no localStorage
    if (isAuthenticated) {
        salvarPreferenciaNoBanco('contraste', tipo);
    } else {
        localStorage.setItem('modoContraste', tipo);
    }
    
    document.getElementById('contraste-menu').classList.add('hidden');
}

// --- GESTÃO DE EVENTOS (FECHAR MENUS) ---
window.addEventListener('click', function(e) {
    const daltMenu = document.getElementById('daltonismo-menu');
    const contMenu = document.getElementById('contraste-menu');
    const perfMenu = document.getElementById('perfil-menu');
    const isButton = e.target.closest('button');

    if (!isButton) {
        if (daltMenu) daltMenu.classList.add('hidden');
        if (contMenu) contMenu.classList.add('hidden');
        if (perfMenu) perfMenu.classList.add('hidden');
    }
});

// --- LÓGICA DE PASSOS DO REGISTO ---
function goToStep(step) {
    const steps = ['step1', 'step2', 'step3'];
    steps.forEach(s => {
        const el = document.getElementById(s);
        if (el) el.classList.add('hidden');
    });
    
    const target = document.getElementById('step' + step);
    if (target) target.classList.remove('hidden');

    const d2 = document.getElementById('dot2');
    const l1 = document.getElementById('line1');
    const d3 = document.getElementById('dot3');
    const l2 = document.getElementById('line2');

    if (d2 && l1) {
        d2.classList.toggle('active', step >= 2);
        l1.classList.toggle('active', step >= 2);
    }
    if (d3 && l2) {
        d3.classList.toggle('active', step >= 3);
        l2.classList.toggle('active', step >= 3);
    }
}

// --- SIMULADOR PHISHING ---
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

// --- INICIALIZAÇÃO ---
document.addEventListener('DOMContentLoaded', () => {
    // Verificar se o utilizador está autenticado
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    // Se está autenticado, os filtros já foram injectados pelo Django
    // Limpar localStorage para não interferer com outro utilizador
    if (isAuthenticated) {
        localStorage.removeItem('modoDaltonismo');
        localStorage.removeItem('modoContraste');
    } else {
        // Utilizador não autenticado: aplicar filtros do localStorage se existirem
        const daltSalvo = localStorage.getItem('modoDaltonismo');
        if (daltSalvo && daltSalvo !== 'normal') {
            document.body.classList.add(daltSalvo);
        }
        
        const contSalvo = localStorage.getItem('modoContraste');
        if (contSalvo && contSalvo !== 'normal') {
            document.body.classList.add(contSalvo);
        }
    }
});