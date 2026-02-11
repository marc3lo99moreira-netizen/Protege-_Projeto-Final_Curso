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

// Executa assim que o HTML básico estiver pronto (mais rápido que window.onload)
document.addEventListener('DOMContentLoaded', aplicarPreferencias);

// --- LÓGICA DE PASSOS DO REGISTO ---
function goToStep(step) {
    // Esconder todos os passos
    const s1 = document.getElementById('step1');
    const s2 = document.getElementById('step2');
    const s3 = document.getElementById('step3');

    if (s1 && s2 && s3) {
        s1.classList.add('hidden');
        s2.classList.add('hidden');
        s3.classList.add('hidden');
        document.getElementById('step' + step).classList.remove('hidden');
    }

    // Atualizar visual da barra de progresso
    const d2 = document.getElementById('dot2');
    const l1 = document.getElementById('line1');
    const d3 = document.getElementById('dot3');
    const l2 = document.getElementById('line2');

    if (d2 && l1 && d3 && l2) {
        d2.classList.toggle('active', step >= 2);
        l1.classList.toggle('active', step >= 2);
        d3.classList.toggle('active', step >= 3);
        l2.classList.toggle('active', step >= 3);
    }
}

document.querySelectorAll('.phishing-trigger').forEach(el => {
            el.addEventListener('click', () => {
                const info = el.getAttribute('data-info');
                const box = document.getElementById('info-box');
                const text = document.getElementById('info-text');
                
                text.innerText = info;
                box.classList.remove('hidden');
                
                // Esconde após 5 segundos
                setTimeout(() => box.classList.add('hidden'), 5000);
            });
        });


function PerfilMenu() {

    document.getElementById('contraste-menu').classList.add('hidden');
    document.getElementById('daltonismo-menu').classList.add('hidden');

    const menu = document.getElementById('perfil-menu');
    if (menu){
        menu.classList.toggle('hidden');
    }
}
