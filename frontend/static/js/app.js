// app.js — Lógica principal da interface galFlowAI

// Carregar preferências
const PREFS_KEY = "galflowai_prefs";
const prefsDefault = {
  voz: "feminino",
  velocidade: 1.0,
  duracao: 30,
  estilo: "animado",
  nivel_log: "info",
  tema: "dark",
  ultimo_briefing: ""
};

function carregarPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY)) || prefsDefault;
  } catch {
    return prefsDefault;
  }
}

function salvarPrefs(prefs) {
  localStorage.setItem(PREFS_KEY, JSON.stringify({...prefsDefault, ...prefs}));
}

// Estado da aplicação
const state = {
  briefing: "",
  projeto_id: null,
  jobs: [],
  currentStep: 1,
  progress: 0,
  logs: []
};

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
  const prefs = carregarPrefs();
  
  // Preencher briefing salvo
  const briefingInput = document.getElementById('briefing-input');
  if (prefs.ultimo_briefing) {
    briefingInput.value = prefs.ultimo_briefing;
    updateCharCount();
  }
  
  // Event listeners
  briefingInput.addEventListener('input', updateCharCount);
  document.getElementById('btn-create').addEventListener('click', criarComercial);
  document.getElementById('btn-novo').addEventListener('click', novoProjeto);
  
  // Sugestões rápidas
  document.querySelectorAll('.suggestion').forEach(btn => {
    btn.addEventListener('click', () => {
      briefingInput.value = btn.textContent;
      updateCharCount();
    });
  });
  
  // Filtros de log
  document.querySelectorAll('.log-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.log-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filtrarLogs(btn.dataset.level);
    });
  });
  
  // Conectar WebSocket
  conectarWebSocket();
  
  console.log('galFlowAI carregado');
});

function updateCharCount() {
  const len = document.getElementById('briefing-input').value.length;
  document.getElementById('char-count').textContent = len;
  
  // Validação
  const btn = document.getElementById('btn-create');
  if (len < 20) {
    btn.disabled = true;
    btn.title = "Mínimo 20 caracteres";
  } else if (len > 500) {
    btn.disabled = true;
    btn.title = "Máximo 500 caracteres";
  } else {
    btn.disabled = false;
    btn.title = "";
  }
}

async function criarComercial() {
  const briefing = document.getElementById('briefing-input').value;
  if (!briefing || briefing.length < 20) {
    toast('Briefing deve ter pelo menos 20 caracteres', 'aviso');
    return;
  }
  
  // Salvar preferência
  salvarPrefs({ ultimo_briefing: briefing });
  
  // Atualizar UI
  state.currentStep = 2;
  updateSteps();
  document.getElementById('btn-create').classList.add('pulse');
  
  try {
    const response = await fetch('/api/criar-comercial', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ briefing })
    });
    
    if (!response.ok) throw new Error('Erro ao criar comercial');
    
    const data = await response.json();
    state.projeto_id = data.projeto_id;
    
    toast('Comercial criado com sucesso!', 'sucesso');
  } catch (error) {
    toast(`Erro: ${error.message}`, 'erro');
    state.currentStep = 1;
    updateSteps();
  } finally {
    document.getElementById('btn-create').classList.remove('pulse');
  }
}

function updateSteps() {
  document.querySelectorAll('.step').forEach(step => {
    const stepNum = parseInt(step.dataset.step);
    step.classList.toggle('active', stepNum === state.currentStep);
  });
}

function novoProjeto() {
  state.briefing = "";
  state.projeto_id = null;
  state.currentStep = 1;
  document.getElementById('briefing-input').value = "";
  updateCharCount();
  updateSteps();
  toast('Novo projeto iniciado', 'info');
}

function toast(msg, tipo = "info", duracao = 4000) {
  const container = document.getElementById('toast-container');
  const el = document.createElement('div');
  el.className = `toast toast-${tipo}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), duracao);
}

function filtrarLogs(level) {
  const logs = state.logs;
  const logContent = document.getElementById('log-content');
  logContent.innerHTML = '';
  
  const filtered = level === 'all' ? logs : logs.filter(l => l.nivel === level);
  filtered.forEach(log => {
    const div = document.createElement('div');
    div.textContent = `[${log.ts}] ${log.nivel}: ${log.msg}`;
    logContent.appendChild(div);
  });
}

function conectarWebSocket() {
  const ws = new WebSocket('ws://localhost:7860/ws/status');
  
  ws.onopen = () => console.log('WebSocket conectado');
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.tipo === 'log') {
      state.logs.push(data);
      if (state.logs.length > 100) state.logs.shift();
      filtrarLogs(document.querySelector('.log-filter.active').dataset.level);
    } else if (data.tipo === 'progresso') {
      state.progress = data.progresso;
      updateProgressBar(data);
    }
  };
  ws.onclose = () => setTimeout(conectarWebSocket, 5000);
}

function updateProgressBar(data) {
  const bar = document.getElementById('progress-bar').querySelector('.progress-fill');
  bar.style.width = `${data.progresso}%`;
  
  const label = data.etapa ? `${data.etapa}: ${data.progresso}%` : `${data.progresso}%`;
  bar.title = label;
}
