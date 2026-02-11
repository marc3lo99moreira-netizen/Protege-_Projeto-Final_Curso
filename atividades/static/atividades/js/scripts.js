// --- LÓGICA DO SIMULADOR (PHISHING) ---
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
// --- FUNÇÕES DE CONTROLO DE MENUS ---
function toggleDaltonismoMenu() {
    document.getElementById('contraste-menu').classList.add('hidden');
    const menu = document.getElementById('daltonismo-menu');
    menu.classList.toggle('hidden');
}

function toggleContrasteMenu() {
    document.getElementById('daltonismo-menu').classList.add('hidden');
    const menu = document.getElementById('contraste-menu');
    menu.classList.toggle('hidden');
}

// --- FUNÇÕES DE APLICAÇÃO DE FILTROS ---
function setDaltonismo(tipo) {
    document.body.classList.remove('protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia');
    if (tipo !== 'normal') {
        document.body.classList.add(tipo);
    }
    localStorage.setItem('modoDaltonismo', tipo);
    document.getElementById('daltonismo-menu').classList.add('hidden');
}

function setContraste(tipo) {
    document.body.classList.remove('alto-contraste', 'contraste-invertido', 'modo-escuro');
    if (tipo !== 'normal') {
        document.body.classList.add(tipo);
    }
    localStorage.setItem('modoContraste', tipo);
    document.getElementById('contraste-menu').classList.add('hidden');
}

// --- GESTÃO DE EVENTOS (FECHAR MENUS) ---
window.addEventListener('click', function(e) {
    const daltMenu = document.getElementById('daltonismo-menu');
    const contMenu = document.getElementById('contraste-menu');
    const isButton = e.target.closest('button');

    if (daltMenu && contMenu && !daltMenu.contains(e.target) && !contMenu.contains(e.target) && !isButton) {
        daltMenu.classList.add('hidden');
        contMenu.classList.add('hidden');
    }
});

// --- FUNÇÃO PARA APLICAR FILTROS IMEDIATAMENTE ---
function aplicarPreferencias() {
    const daltSalvo = localStorage.getItem('modoDaltonismo');
    if (daltSalvo && daltSalvo !== 'normal') {
        document.body.classList.add(daltSalvo);
    }
    
    const contSalvo = localStorage.getItem('modoContraste');
    if (contSalvo && contSalvo !== 'normal') {
        document.body.classList.add(contSalvo);
    }
}
// Nota: A função PerfilMenu() deve ficar onde estiver o teu Header (normalmente num base.html)