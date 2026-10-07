const API = 'http://127.0.0.1:5000';

let etapa = 'representante';
let numero = '';
let rep = null;
let vice = null;
let reps = [];
let vices = [];

function show(id) {
    document.querySelectorAll('.tela').forEach(x => x.classList.add('hidden'));

    document.getElementById(id).classList.remove('hidden');

    if (id === 'votacao') {
        loadCandidates();
        resetUrna();
    }

    if (id === 'resultado') {
        carregarResultados();
    }
}

async function req(url, opt = {}) {
    const r = await fetch(API + url, {
        headers: {
            'Content-Type': 'application/json'
        },
        ...opt
    });

    const d = await r.json();

    if (!r.ok) {
        throw new Error(d.erro || 'Erro');
    }

    return d;
}

formEleitor.onsubmit = async e => {
    e.preventDefault();

    try {
        await req('/eleitores', {
            method: 'POST',
            body: JSON.stringify({
                nome: nomeEleitor.value,
                matricula: matriculaEleitor.value
            })
        });

        e.target.reset();
        loadEleitores();

    } catch (x) {
        alert(x.message);
    }
};

formRepresentante.onsubmit = async e => {
    e.preventDefault();

    try {
        await req('/representantes', {
            method: 'POST',
            body: JSON.stringify({
                nome: nomeRepresentante.value,
                numero: +numeroRepresentante.value
            })
        });

        e.target.reset();
        loadReps();

    } catch (x) {
        alert(x.message);
    }
};

formVice.onsubmit = async e => {
    e.preventDefault();

    try {
        await req('/vices', {
            method: 'POST',
            body: JSON.stringify({
                nome: nomeVice.value,
                numero: +numeroVice.value
            })
        });

        e.target.reset();
        loadVices();

    } catch (x) {
        alert(x.message);
    }
};

async function loadEleitores() {
    try {
        let d = await req('/eleitores');

        listaEleitores.innerHTML = d
            .map(e =>
                `<div class="item">
                    ${e.nome} — ${e.matricula} — ${e.votou ? 'já votou' : 'não votou'}
                </div>`
            )
            .join('');

    } catch {
        listaEleitores.innerHTML =
            '<div class="item">Banco não conectado.</div>';
    }
}

async function loadReps() {
    try {
        let d = await req('/representantes');

        listaRepresentantes.innerHTML = d
            .map(c =>
                `<div class="item">
                    ${String(c.numero).padStart(2, '0')} — ${c.nome}
                </div>`
            )
            .join('');

    } catch {
        listaRepresentantes.innerHTML =
            '<div class="item">Banco não conectado.</div>';
    }
}

async function loadVices() {
    try {
        let d = await req('/vices');

        listaVices.innerHTML = d
            .map(c =>
                `<div class="item">
                    ${String(c.numero).padStart(2, '0')} — ${c.nome}
                </div>`
            )
            .join('');

    } catch {
        listaVices.innerHTML =
            '<div class="item">Banco não conectado.</div>';
    }
}

async function loadCandidates() {
    try {
        reps = await req('/representantes');
        vices = await req('/vices');

    } catch (e) {
        mensagemVoto.textContent = e.message;
    }
}

function digitar(n) {
    if (numero.length >= 2) {
        return;
    }

    numero += n;

    refresh();

    if (numero.length === 2) {
        findCandidate();
    }
}

function refresh() {
    let d = document.querySelectorAll('.digit');

    d[0].textContent = numero[0] || '';
    d[1].textContent = numero[1] || '';
}

function findCandidate() {
    let list = etapa === 'representante' ? reps : vices;

    let c = list.find(x => +x.numero === +numero);

    dadosCandidato.innerHTML = c
        ? `<div class="name">${c.nome}</div>
           <div class="num">
               Número: ${String(c.numero).padStart(2, '0')}
           </div>`
        : `<div class="name">NÚMERO INVÁLIDO</div>
           <div class="num">Pressione CORRIGE.</div>`;
}

function corrigir() {
    numero = '';

    refresh();

    dadosCandidato.innerHTML =
        '<p>Digite o número do candidato.</p>';

    mensagemVoto.textContent = '';
}

function branco() {
    mensagemVoto.textContent =
        'Voto em branco não está habilitado nesta versão didática.';
}

async function confirmar() {
    if (numero.length !== 2) {
        mensagemVoto.textContent =
            'Digite os dois números.';

        return;
    }

    let list = etapa === 'representante' ? reps : vices;

    let c = list.find(x => +x.numero === +numero);

    if (!c) {
        mensagemVoto.textContent =
            'Candidato inválido.';

        return;
    }

    if (etapa === 'representante') {
        rep = c;
        etapa = 'vice';
        numero = '';

        cargoAtual.textContent = 'VICE-REPRESENTANTE';

        refresh();

        dadosCandidato.innerHTML =
            '<p>Agora digite o número do vice-representante.</p>';

        return;
    }

    vice = c;

    await vote();
}

async function vote() {
    if (!matriculaVotante.value.trim()) {
        mensagemVoto.textContent =
            'Informe a matrícula.';

        return;
    }

    try {
        let d = await req('/votar', {
            method: 'POST',
            body: JSON.stringify({
                matricula: matriculaVotante.value.trim(),
                representante_id: rep.id,
                vice_id: vice.id
            })
        });

        dadosCandidato.innerHTML =
            `<div class="name">FIM</div>
             <div class="num">Voto registrado com sucesso.</div>`;

        mensagemVoto.textContent = d.mensagem;

        loadEleitores();

        setTimeout(() => {
            resetUrna();
            matriculaVotante.value = '';
        }, 1600);

    } catch (e) {
        mensagemVoto.textContent = e.message;
    }
}

function resetUrna() {
    etapa = 'representante';
    numero = '';
    rep = null;
    vice = null;

    cargoAtual.textContent = 'REPRESENTANTE';

    refresh();

    dadosCandidato.innerHTML =
        '<p>Digite o número do candidato.</p>';
}

async function carregarResultados() {
    try {
        let d = await req('/resultados');

        resultadoRepresentantes.innerHTML =
            `<table>
                <tr>
                    <th>Número</th>
                    <th>Candidato</th>
                    <th>Votos</th>
                </tr>

                ${d.representantes
                    .map(r =>
                        `<tr>
                            <td>${String(r.numero).padStart(2, '0')}</td>
                            <td>${r.nome}</td>
                            <td>${r.votos}</td>
                        </tr>`
                    )
                    .join('')}
            </table>`;

        resultadoVices.innerHTML =
            `<table>
                <tr>
                    <th>Número</th>
                    <th>Candidato</th>
                    <th>Votos</th>
                </tr>

                ${d.vices
                    .map(r =>
                        `<tr>
                            <td>${String(r.numero).padStart(2, '0')}</td>
                            <td>${r.nome}</td>
                            <td>${r.votos}</td>
                        </tr>`
                    )
                    .join('')}
            </table>`;

    } catch {
        resultadoRepresentantes.innerHTML =
            'Banco não conectado.';

        resultadoVices.innerHTML =
            'Banco não conectado.';
    }
}

loadEleitores();
loadReps();
loadVices();