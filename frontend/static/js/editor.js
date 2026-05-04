// editor.js — Editor de roteiro inline

class SceneEditor {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.cenas = [];
    this.init();
  }
  
  init() {
    this.render();
  }
  
  carregarCenas(cenas) {
    this.cenas = cenas || [];
    this.render();
  }
  
  render() {
    if (!this.container) return;
    this.container.innerHTML = '';
    
    this.cenas.forEach((cena, index) => {
      const card = this.criarCardCena(cena, index);
      this.container.appendChild(card);
    });
    
    // Botão adicionar cena
    const addBtn = document.createElement('button');
    addBtn.className = 'suggestion';
    addBtn.textContent = '+ Adicionar cena';
    addBtn.addEventListener('click', () => this.adicionarCena());
    this.container.appendChild(addBtn);
  }
  
  criarCardCena(cena, index) {
    const card = document.createElement('div');
    card.className = 'card scene-card';
    card.draggable = true;
    card.dataset.index = index;
    
    // Título editável
    const title = document.createElement('input');
    title.type = 'text';
    title.value = cena.titulo || `Cena ${index + 1}`;
    title.className = 'scene-title';
    title.addEventListener('change', (e) => {
      this.cenas[index].titulo = e.target.value;
    });
    
    // Descrição editável
    const desc = document.createElement('textarea');
    desc.value = cena.descricao || '';
    desc.rows = 3;
    desc.className = 'scene-desc';
    desc.addEventListener('change', (e) => {
      this.cenas[index].descricao = e.target.value;
    });
    
    // Duração
    const durationDiv = document.createElement('div');
    durationDiv.className = 'config-row';
    [3, 5, 8].forEach(d => {
      const btn = document.createElement('button');
      btn.className = `btn-duration ${cena.duracao === d ? 'active' : ''}`;
      btn.textContent = `${d}s`;
      btn.addEventListener('click', () => {
        this.cenas[index].duracao = d;
        this.render();
      });
      durationDiv.appendChild(btn);
    });
    
    // Botões de ação
    const actions = document.createElement('div');
    actions.style.marginTop = '0.5rem';
    
    if (index > 0) {
      const upBtn = document.createElement('button');
      upBtn.textContent = '↑ Mover';
      upBtn.className = 'suggestion';
      upBtn.addEventListener('click', () => this.moverCena(index, index - 1));
      actions.appendChild(upBtn);
    }
    
    if (index < this.cenas.length - 1) {
      const downBtn = document.createElement('button');
      downBtn.textContent = '↓ Mover';
      downBtn.className = 'suggestion';
      downBtn.addEventListener('click', () => this.moverCena(index, index + 1));
      actions.appendChild(downBtn);
    }
    
    const removeBtn = document.createElement('button');
    removeBtn.textContent = '🗑 Remover';
    removeBtn.className = 'suggestion';
    removeBtn.style.color = 'var(--error)';
    removeBtn.addEventListener('click', () => this.removerCena(index));
    actions.appendChild(removeBtn);
    
    card.appendChild(title);
    card.appendChild(desc);
    card.appendChild(durationDiv);
    card.appendChild(actions);
    
    // Drag and drop
    card.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', index);
      card.classList.add('dragging');
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('dragging');
    });
    
    return card;
  }
  
  adicionarCena() {
    this.cenas.push({
      titulo: `Cena ${this.cenas.length + 1}`,
      descricao: '',
      duracao: 5
    });
    this.render();
  }
  
  removerCena(index) {
    this.cenas.splice(index, 1);
    this.render();
  }
  
  moverCena(fromIndex, toIndex) {
    const [cena] = this.cenas.splice(fromIndex, 1);
    this.cenas.splice(toIndex, 0, cena);
    this.render();
  }
  
  // Drag and drop zone
  setupDropZone() {
    const zone = document.createElement('div');
    zone.className = 'drop-zone';
    zone.textContent = 'Solte aqui para reordenar';
    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('drag-over');
    });
    zone.addEventListener('dragleave', () => {
      zone.classList.remove('drag-over');
    });
    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('drag-over');
      const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
      // Determine toIndex based on position
      // Simplified for now
    });
    this.container.appendChild(zone);
  }
  
  getCenas() {
    return this.cenas;
  }
}

// Exportar
window.SceneEditor = SceneEditor;
