// progress.js — Barras de progresso realistas

const ETAPAS = [
  { id: 'projeto',   label: 'Criando projeto',     peso: 5  },
  { id: 'roteiro',   label: 'Gerando roteiro',      peso: 20 },
  { id: 'cenas',     label: 'Dividindo em cenas',   peso: 10 },
  { id: 'prompts',   label: 'Construindo prompts',  peso: 10 },
  { id: 'render',    label: 'Renderizando cenas',   peso: 35 },
  { id: 'narracao',  label: 'Gerando narração',     peso: 15 },
  { id: 'montagem',  label: 'Montagem final',       peso: 5  },
];

// Calcular progresso global baseado no progresso de cada etapa
function calcularProgressoGlobal(etapa_atual, progresso_etapa) {
  let progresso_acumulado = 0;
  let peso_total = ETAPAS.reduce((sum, e) => sum + e.peso, 0);
  
  for (let etapa of ETAPAS) {
    if (etapa.id === etapa_atual) {
      // Progresso parcial desta etapa
      progresso_acumulado += (progresso_etapa / 100) * etapa.peso;
      break;
    } else {
      progresso_acumulado += etapa.peso;
    }
  }
  
  return Math.round((progresso_acumulado / peso_total) * 100);
}

// WebSocket handler para progresso
function handleProgresso(data) {
  const { etapa, sub_progresso, tempo_decorrido, tempo_estimado } = data;
  
  // Atualizar barra principal
  const progresso_global = calcularProgressoGlobal(etapa, sub_progresso);
  updateProgressBar(progresso_global, etapa);
  
  // Mostrar detalhes
  if (tempo_estimado) {
    updateTempoEstimado(tempo_estimado, tempo_decorrido);
  }
}

function updateProgressBar(progresso, etapa_atual) {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  
  const fill = bar.querySelector('.progress-fill') || bar;
  fill.style.width = `${progresso}%`;
  fill.title = `Progresso: ${progresso}% - ${etapa_atual || ''}`;
}

function updateTempoEstimado(estimado, decorrido) {
  const logContent = document.getElementById('log-content');
  if (!logContent) return;
  
  const ultimaLinha = logContent.lastElementChild;
  if (ultimaLinha && ultimaLinha.classList.contains('tempo-info')) {
    ultimaLinha.textContent = `Tempo: ${decorrido}s / ${estimado}s`;
  } else {
    const div = document.createElement('div');
    div.className = 'tempo-info';
    div.style.color = 'var(--text-muted)';
    div.style.fontSize = '0.8rem';
    div.textContent = `Tempo: ${decorrido}s / ${estimado}s`;
    logContent.appendChild(div);
  }
}

// Exportar para uso global
window.ETAPAS = ETAPAS;
window.calcularProgressoGlobal = calcularProgressoGlobal;
window.handleProgresso = handleProgresso;
