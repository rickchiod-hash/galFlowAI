// ws.js — WebSocket para status em tempo real.

class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectDelay = 5000;
    this.maxReconnectDelay = 30000;
    this.listeners = {
      'log': [],
      'progresso': [],
      'job_update': [],
      'open': [],
      'close': [],
      'error': []
    };
    
    this.conectar();
  }
  
  conectar() {
    try {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = (event) => {
        console.log('WebSocket conectado:', this.url);
        this.listeners['open'].forEach(cb => cb(event));
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const tipo = data.tipo || 'unknown';
          if (this.listeners[tipo]) {
            this.listeners[tipo].forEach(cb => cb(data));
          }
        } catch (e) {
          console.error('Erro ao parser mensagem WebSocket:', e);
        }
      };
      
      this.ws.onclose = (event) => {
        console.log('WebSocket desconectado. Reconectando...');
        this.listeners['close'].forEach(cb => cb(event));
        setTimeout(() => this.conectar(), this.reconnectDelay);
      };
      
      this.ws.onerror = (event) => {
        console.error('Erro WebSocket:', event);
        this.listeners['error'].forEach(cb => cb(event));
      };
    } catch (e) {
      console.error('Falha ao conectar WebSocket:', e);
      setTimeout(() => this.conectar(), this.reconnectDelay);
    }
  }
  
  on(tipo, callback) {
    if (this.listeners[tipo]) {
      this.listeners[tipo].push(callback);
    }
  }
  
  of(tipo, callback) {
    if (this.listeners[tipo]) {
      this.listeners[tipo] = this.listeners[tipo].filter(cb => cb !== callback);
    }
  }
  
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(typeof data === 'string' ? data : JSON.stringify(data));
    } else {
      console.warn('WebSocket não está conectado');
    }
  }
  
  close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Criar instância global
const wsClient = new WebSocketClient('ws://localhost:7860/ws/status');

// Handlers padrão
wsClient.on('log', (data) => {
  const event = new CustomEvent('ws-log', { detail: data });
  document.dispatchEvent(event);
});

wsClient.on('progresso', (data) => {
  const event = new CustomEvent('ws-progress', { detail: data });
  document.dispatchEvent(event);
});

wsClient.on('job_update', (data) => {
  const event = new CustomEvent('ws-job', { detail: data });
  document.dispatchEvent(event);
});

// Exportar
window.WebSocketClient = WebSocketClient;
window.wsClient = wsClient;
