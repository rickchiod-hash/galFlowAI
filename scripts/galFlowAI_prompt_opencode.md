# galFlowAI — Prompt Mestre para OpenCode Hy3
> Versão: 2.0 | Base: MVP Mock funcional rodando em http://127.0.0.1:7860
> Objetivo: Transformar o galFlowAI em um estúdio profissional de comerciais com IA, 100% local, zero custo, robusto e com UX premium.

---

## CONTEXTO ATUAL (ponto de partida)

```
Estado: MVP Mock funcionando
- Interface Gradio rodando em http://127.0.0.1:7860
- Pipeline: briefing → roteiro → cenas → storyboard FFmpeg → MP4
- Status retorna: "galFlowAI: Comercial criado com sucesso! (MVP Mock)"
- WanGP ainda NÃO integrado (storyboard estático apenas)
- Vídeos salvos em: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\projects\
- GPU: NVIDIA GTX 1660 Super (6 GB VRAM)
- OS: Windows 10/11, Disco K:
- Python 3.10+, Gradio, FFmpeg disponíveis
```

---

## REGRAS ABSOLUTAS (não quebrar)

```
✅ TUDO roda em K: — jamais salvar em C:
✅ Zero dependências pagas ou APIs externas com custo
✅ Não quebrar WanGP/FramePack existentes em K:
✅ Modelo padrão: 1.3B (seguro para 6 GB VRAM) — 14B bloqueado no modo seguro
✅ Fallback FFmpeg sempre disponível se WanGP falhar
✅ 100% em português brasileiro (UI, logs, erros, comentários)
✅ Cada PR deve ter testes automatizados passando antes do merge
```

---

## ARQUITETURA GERAL — NOVA ESTRUTURA

Quebrar o projeto em camadas independentes e bem separadas:

```
galFlowAI/
├── cmd/                        ← [NOVO] Executáveis Go
│   ├── server/main.go          ← Servidor Go (substitui uvicorn/gradio server)
│   ├── worker/main.go          ← Worker Go para processar jobs da fila
│   └── cli/main.go             ← CLI Go para uso sem interface
│
├── core/                       ← [NOVO] Engine Go — alta performance
│   ├── queue/                  ← Fila de jobs persistente (BoltDB ou arquivo JSON)
│   ├── ffmpeg/                 ← Wrapper Go para FFmpeg
│   ├── hardware/               ← Detecção GPU/VRAM/RAM em Go
│   ├── watcher/                ← Watcher de projetos em Go
│   └── bridge/                 ← Bridge Go ↔ Python (exec subprocess)
│
├── app/                        ← Python — lógica de IA e pipelines
│   ├── main.py                 ← Interface web (migrar de Gradio para FastAPI+HTML)
│   ├── config.py
│   ├── hardware.py
│   ├── logging_config.py
│   ├── project_manager.py
│   ├── safety.py
│   ├── adapters/
│   │   ├── ffmpeg_adapter.py
│   │   ├── wangp_adapter.py    ← INTEGRAR REAL aqui
│   │   ├── tts_adapter.py      ← IMPLEMENTAR kokoro/pyttsx3
│   │   └── ollama_adapter.py   ← [NOVO] LLM local via Ollama
│   └── pipelines/
│       ├── auto_pipeline.py
│       ├── script_generator.py
│       ├── scene_splitter.py
│       ├── prompt_builder.py
│       └── voice_pipeline.py   ← [NOVO] pipeline de narração
│
├── frontend/                   ← [NOVO] Frontend premium (HTML/CSS/JS puro)
│   ├── index.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css        ← Design system inspirado em Google AI Studio
│   │   │   ├── components.css
│   │   │   └── animations.css
│   │   └── js/
│   │       ├── app.js          ← Lógica principal
│   │       ├── progress.js     ← Barras de progresso realistas
│   │       ├── editor.js       ← Editor de roteiro inline
│   │       └── ws.js           ← WebSocket para status em tempo real
│
├── tests/                      ← Testes completos
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                    ← Scripts de manutenção
│   ├── start_app.bat
│   ├── build_go.bat            ← [NOVO] Compila executáveis Go
│   └── run_tests.bat           ← [NOVO] Roda 100% dos testes
│
└── go.mod                      ← [NOVO] Módulo Go
```

---

## ETAPA 1 — BACKEND GO: Performance e Executável

### Objetivo
Criar o executável Go que serve de espinha dorsal do sistema: gerencia a fila de jobs, serve o frontend, e faz bridge com o Python para as partes de IA.

### Tarefa 1.1 — Inicializar módulo Go
```bash
# No diretório raiz do projeto
go mod init galflowai
```

### Tarefa 1.2 — Servidor HTTP Go (cmd/server/main.go)
```
Requisitos:
- Servir o frontend/ estático em http://localhost:7860
- WebSocket endpoint: /ws/status → emite progresso de jobs em tempo real
- REST API:
  - POST /api/criar-comercial     → recebe briefing, enfileira job
  - GET  /api/projetos            → lista projetos
  - GET  /api/projeto/:id         → detalhes + status
  - GET  /api/projeto/:id/video   → stream do vídeo gerado
  - GET  /api/hardware            → info GPU/VRAM/disco
  - POST /api/cancelar/:id        → cancela job em andamento
- Executar os scripts Python via exec.Command (bridge)
- Logs em português, coloridos no terminal
- Sem dependências externas pesadas — usar apenas stdlib Go + gorilla/websocket
```

### Tarefa 1.3 — Worker Go (cmd/worker/main.go)
```
Requisitos:
- Processar jobs da fila em background (goroutines)
- Emitir progresso via canal interno → WebSocket
- Timeout configurável por job (padrão 30min)
- Retomar jobs interrompidos ao reiniciar
- Matar processo filho Python se job for cancelado
- Log de cada etapa com timestamp
```

### Tarefa 1.4 — Fila persistente (core/queue/)
```go
// Interface mínima necessária:
type Job struct {
    ID        string
    Briefing  string
    Status    string  // "pending" | "running" | "done" | "error" | "cancelled"
    Progress  int     // 0-100
    CreatedAt time.Time
    UpdatedAt time.Time
    ProjectPath string
    ErrorMsg  string
}

// Persistir em K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\state\queue.json
// Sem banco de dados externo — arquivo JSON simples com lock de arquivo
```

### Tarefa 1.5 — Build script (scripts/build_go.bat)
```bat
@echo off
set GOOS=windows
set GOARCH=amd64
go build -o galflowai.exe ./cmd/server/
echo Build concluido: galflowai.exe
```

### Tarefa 1.6 — Testes Go
```
- core/queue: TestEnqueue, TestDequeue, TestPersist, TestResumeAfterCrash
- core/hardware: TestDetectGPU, TestVRAMAvailable
- cmd/server: TestAPIEndpoints (httptest), TestWebSocket
- Cobertura mínima: 80%
- Rodar com: go test ./... -v -cover
```

---

## ETAPA 2 — FRONTEND PREMIUM (inspirado em Google AI Studio + Google Flow)

### Objetivo
Substituir o Gradio por um frontend HTML/CSS/JS próprio, servido pelo Go, com aparência profissional.

### Design System

```css
/* Paleta principal — dark mode como padrão */
--bg-base: #0f0f0f;           /* fundo principal */
--bg-surface: #1a1a1a;        /* cards, painéis */
--bg-elevated: #242424;       /* inputs, dropdowns */
--bg-hover: #2e2e2e;
--accent-primary: #FF6B2B;    /* laranja galFlow (manter identidade) */
--accent-secondary: #FF8C5A;
--accent-glow: rgba(255,107,43,0.15);
--text-primary: #f0f0f0;
--text-secondary: #9a9a9a;
--text-muted: #555;
--border: rgba(255,255,255,0.08);
--border-accent: rgba(255,107,43,0.3);
--success: #22c55e;
--warning: #f59e0b;
--error: #ef4444;
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 16px;
--font: 'Inter', system-ui, sans-serif;
--mono: 'JetBrains Mono', monospace;
```

### Layout da tela principal

```
┌─────────────────────────────────────────────────────────────┐
│ ■ galFlowAI          [Hardware: GTX1660 6GB ✓]  [K: 87GB] │  ← Header fixo
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  SIDEBAR     │          ÁREA PRINCIPAL                      │
│  ─────────   │                                              │
│  + Novo      │  [1. Briefing] → [2. Roteiro] → [3. Gerar]  │
│  ─────────   │                                              │
│  Projetos:   │  ┌─ CARD BRIEFING ────────────────────────┐ │
│  • Medabee   │  │  Descreva seu comercial...              │ │
│  • Proj #2   │  │  [textarea grande, 4 linhas min]        │ │
│  • Proj #3   │  └────────────────────────────────────────┘ │
│              │                                              │
│  ─────────   │  ┌─ CARD CONFIGURAÇÕES ───────────────────┐ │
│  Hardware    │  │  Duração: [15s] [30s] [60s]  Voz: ♂/♀  │ │
│  RAM: 16GB   │  │  Idioma: PT-BR  Estilo: [Animado/Sério] │ │
│  VRAM: 6GB   │  └────────────────────────────────────────┘ │
│  K: 87GB     │                                              │
│              │  [CRIAR COMERCIAL ████████████████]         │
└──────────────┴──────────────────────────────────────────────┘
```

### Componentes obrigatórios a implementar

**A) Painel de Briefing**
```
- Textarea grande com placeholder em PT-BR
- Contador de caracteres (min 20, max 500)
- Sugestões rápidas clicáveis: "Produto físico" | "Serviço" | "Evento" | "App"
- Histórico dos últimos 5 briefings (localStorage)
```

**B) Editor de Roteiro (pós-geração)**
```
- Exibir roteiro gerado em seções editáveis
- Cada cena como card individual:
  ┌─ Cena 1 ────────────────────────┐
  │ [Título editável]               │
  │ [Descrição editável - textarea] │
  │ Duração: [3s] [5s] [8s]        │
  │ [↑ Mover] [↓ Mover] [🗑 Remover]│
  └─────────────────────────────────┘
- Botão "Adicionar cena"
- Botão "Regenerar roteiro" (mantém briefing)
- Botão "Continuar com este roteiro →"
```

**C) Seletor de Voz**
```
- Toggle visual: ♂ Masculino / ♀ Feminino
- Velocidade: [0.8x] [1.0x] [1.2x] [1.5x]
- Botão "Ouvir amostra" (gera 3s de áudio de preview)
- Vozes disponíveis: listar as do pyttsx3/Kokoro instaladas
- Salvar preferência de voz no perfil do usuário
```

**D) Barra de Progresso Realista**
```javascript
// NÃO usar progresso falso/linear
// Cada etapa tem seu próprio progresso real:

const ETAPAS = [
  { id: 'projeto',   label: 'Criando projeto',     peso: 5  },
  { id: 'roteiro',   label: 'Gerando roteiro',      peso: 20 },
  { id: 'cenas',     label: 'Dividindo em cenas',   peso: 10 },
  { id: 'prompts',   label: 'Construindo prompts',  peso: 10 },
  { id: 'render',    label: 'Renderizando cenas',   peso: 35 },  // mais pesado
  { id: 'narracao',  label: 'Gerando narração',     peso: 15 },
  { id: 'montagem',  label: 'Montagem final',       peso: 5  },
];

// Progresso vem via WebSocket — cada etapa emite % real do seu processo
// Ex: render de 4 cenas → 25% por cena → emite 0%, 25%, 50%, 75%, 100% dentro de "render"
// Mostrar: etapa atual + sub-progresso + tempo estimado + tempo decorrido
// Mostrar log ao vivo abaixo da barra (últimas 5 linhas)
```

**E) Player de Resultado**
```
- Reproduzir o vídeo gerado inline (sem download obrigatório)
- Mostrar: duração, tamanho do arquivo, resolução, fps
- Botões: [▶ Assistir] [⬇ Baixar] [🔄 Regerar] [✏ Editar roteiro]
- Miniaturas das cenas abaixo do player
- Compartilhar: copiar caminho do arquivo
```

**F) Painel de Hardware (sidebar)**
```
- GPU: nome + VRAM usada/total + temperatura (se disponível)
- RAM: usada/total
- Disco K:: livre/total
- Modo seguro ON/OFF (bloqueia 14B quando ON)
- Atualizar a cada 10 segundos via polling
- Alertas visuais se VRAM < 1GB ou disco < 10GB
```

**G) Log em tempo real**
```
- Painel expansível na parte inferior
- Filtros: [TODOS] [ERROS] [AVISOS] [INFO]
- Auto-scroll + botão de pausa
- Copiar log completo
- Limpar log
- Nível de detalhe: [Simples] [Detalhado] [Debug]
```

### Animações e micro-interações
```css
/* Inspirado em Google AI Studio — suave, profissional */
- Fade-in de 200ms nos cards ao carregar
- Skeleton loading enquanto dados carregam
- Botão "Criar comercial": pulse animation quando processo ativo
- Progresso: transição suave width com cubic-bezier
- Cards de cena: drag-and-drop para reordenar
- Notificações toast: canto inferior direito, auto-fechar 4s
- Hover nos cards: elevação sutil (box-shadow)
```

---

## ETAPA 3 — INTEGRAÇÃO REAL DO WanGP 1.3B

### Objetivo
Substituir o MVP Mock por geração real de vídeo com o modelo WanGP 1.3B.

### Tarefa 3.1 — Verificação do ambiente WanGP
```python
# app/adapters/wangp_adapter.py — REESCREVER COMPLETO

import subprocess
import os
import json
from pathlib import Path

WANGP_PATH = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/engines/Wan2GP")
PYTHON_ENV = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/envs/studio/python.exe")
VRAM_LIMITE_SEGURO_MB = 5500  # 5.5 GB de 6 GB disponíveis

class WanGPAdapter:
    def __init__(self, logger):
        self.logger = logger
        self.disponivel = self._verificar_instalacao()
    
    def _verificar_instalacao(self) -> bool:
        """Verifica se WanGP está instalado e operacional"""
        checks = [
            WANGP_PATH.exists(),
            (WANGP_PATH / "generate.py").exists(),
            PYTHON_ENV.exists(),
        ]
        return all(checks)
    
    def gerar_cena(self, prompt: str, duracao_seg: int, 
                   output_path: Path, progress_callback=None) -> bool:
        """
        Gera uma cena de vídeo com WanGP 1.3B
        - prompt: descrição da cena em inglês (traduzido antes de chamar)
        - duracao_seg: 3, 5 ou 8 segundos
        - output_path: onde salvar o .mp4 da cena
        - progress_callback: fn(percent: int, msg: str)
        """
        if not self.disponivel:
            self.logger.warning("WanGP não disponível — usando fallback FFmpeg")
            return False
        
        vram_disponivel = self._checar_vram_mb()
        if vram_disponivel < 4000:
            self.logger.warning(f"VRAM insuficiente: {vram_disponivel}MB — usando fallback")
            return False
        
        cmd = [
            str(PYTHON_ENV),
            str(WANGP_PATH / "generate.py"),
            "--prompt", prompt,
            "--duration", str(duracao_seg),
            "--output", str(output_path),
            "--model", "1.3B",
            "--steps", "20",          # qualidade/velocidade balanceados
            "--guidance", "7.5",
        ]
        
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8'
            )
            for line in proc.stdout:
                line = line.strip()
                if progress_callback and "%" in line:
                    # Parsear progresso do output do WanGP
                    try:
                        pct = int(line.split("%")[0].split()[-1])
                        progress_callback(pct, f"WanGP: {line}")
                    except:
                        pass
                self.logger.debug(f"WanGP: {line}")
            
            proc.wait()
            return proc.returncode == 0 and output_path.exists()
        except Exception as e:
            self.logger.error(f"Erro no WanGP: {e}")
            return False
    
    def _checar_vram_mb(self) -> int:
        """Retorna VRAM livre em MB via nvidia-smi"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                capture_output=True, text=True
            )
            return int(result.stdout.strip())
        except:
            return 0
```

### Tarefa 3.2 — Tradução de prompts PT-BR → EN
```python
# app/adapters/translator_adapter.py — [NOVO]
# Usar modelo de tradução local via Ollama (sem custo)

class TranslatorAdapter:
    """
    Traduz prompts de cenas do PT-BR para EN para o WanGP.
    Usa Ollama local com modelo leve (ex: gemma:2b ou llama3.2:1b)
    Fallback: tradução por dicionário de termos comuns de comercial
    """
    
    FALLBACK_DICT = {
        "produto": "product", "venda": "sale", "boneco": "figure",
        "colecionável": "collectible", "animado": "animated",
        # ... expandir conforme uso
    }
    
    def traduzir(self, texto_ptbr: str) -> str:
        # 1. Tentar Ollama
        # 2. Fallback: tradução básica por dicionário
        pass
```

### Tarefa 3.3 — Fallback gracioso
```python
# Lógica de fallback em auto_pipeline.py:
# 1. Tentar WanGP → sucesso → usar vídeo gerado
# 2. WanGP falhar → usar FFmpeg storyboard animado (melhorado)
# 3. Storyboard: fundo colorido + texto da cena + transições suaves
# 4. Sempre gerar um vídeo funcional — nunca retornar "sem resultado"
```

---

## ETAPA 4 — TTS: NARRAÇÃO OFFLINE

### Tarefa 4.1 — tts_adapter.py COMPLETO
```python
# app/adapters/tts_adapter.py — REESCREVER

class TTSAdapter:
    """
    Gerador de narração offline com suporte a voz masculina e feminina.
    Prioridade: Kokoro → pyttsx3 → silêncio (sem falha)
    """
    
    def __init__(self, logger, voz: str = "feminino", velocidade: float = 1.0):
        self.logger = logger
        self.voz = voz          # "masculino" ou "feminino"
        self.velocidade = velocidade
        self.engine = self._inicializar_engine()
    
    def _inicializar_engine(self):
        """Tenta Kokoro primeiro, depois pyttsx3"""
        # Tentar Kokoro (melhor qualidade)
        try:
            from kokoro import KPipeline
            pipeline = KPipeline(lang_code='p')  # PT-BR
            self.logger.info("TTS: usando Kokoro (alta qualidade)")
            return ("kokoro", pipeline)
        except ImportError:
            pass
        
        # Fallback pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            vozes = engine.getProperty('voices')
            # Selecionar voz PT-BR masculina ou feminina
            voz_selecionada = self._selecionar_voz_ptbr(vozes, self.voz)
            if voz_selecionada:
                engine.setProperty('voice', voz_selecionada.id)
            engine.setProperty('rate', int(150 * self.velocidade))
            self.logger.info("TTS: usando pyttsx3")
            return ("pyttsx3", engine)
        except Exception as e:
            self.logger.warning(f"TTS: sem engine disponível — narração silenciosa ({e})")
            return ("silencio", None)
    
    def _selecionar_voz_ptbr(self, vozes, genero: str):
        """Seleciona a melhor voz PT-BR disponível"""
        for v in vozes:
            nome = (v.name or "").lower()
            lang = (str(v.languages) or "").lower()
            if "pt" in lang or "brazil" in nome or "brasil" in nome:
                if genero == "feminino" and any(x in nome for x in ["female", "zira", "maria"]):
                    return v
                if genero == "masculino" and any(x in nome for x in ["male", "daniel", "paulo"]):
                    return v
        # Retorna qualquer PT-BR disponível
        for v in vozes:
            if "pt" in str(v.languages).lower():
                return v
        return None
    
    def gerar_audio(self, texto: str, output_path: Path) -> bool:
        """Gera arquivo WAV/MP3 da narração"""
        tipo, engine = self.engine
        
        if tipo == "kokoro":
            return self._gerar_kokoro(engine, texto, output_path)
        elif tipo == "pyttsx3":
            return self._gerar_pyttsx3(engine, texto, output_path)
        else:
            # Gerar silêncio de duração proporcional ao texto
            return self._gerar_silencio(texto, output_path)
    
    def preview_3s(self, output_path: Path) -> bool:
        """Gera 3 segundos de áudio de preview da voz selecionada"""
        texto = "Olá, esta é a voz selecionada para o seu comercial."
        return self.gerar_audio(texto, output_path)
```

### Tarefa 4.2 — Sincronização áudio + vídeo
```python
# Em ffmpeg_adapter.py — adicionar mixagem:
def mixar_audio_video(video_path, audio_path, output_path):
    """Combina narração com vídeo, ajustando duração automaticamente"""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",             # termina quando o menor acabar
        "-filter:a", "afade=t=out:st=0:d=0.5",  # fade out suave no áudio
        str(output_path)
    ]
```

---

## ETAPA 5 — TESTES 100% (Cobertura Completa)

### Estrutura de testes

```
tests/
├── unit/
│   ├── test_script_generator.py
│   ├── test_scene_splitter.py
│   ├── test_prompt_builder.py
│   ├── test_ffmpeg_adapter.py
│   ├── test_tts_adapter.py
│   ├── test_wangp_adapter.py
│   ├── test_project_manager.py
│   └── test_safety.py
│
├── integration/
│   ├── test_pipeline_completa.py      ← testa fluxo end-to-end
│   ├── test_fallback_wangp.py         ← WanGP falha → FFmpeg assume
│   ├── test_fallback_tts.py           ← Kokoro falha → pyttsx3 assume
│   ├── test_queue_persistencia.py     ← Job sobrevive a crash
│   └── test_websocket_progresso.py    ← WebSocket emite eventos certos
│
└── e2e/
    ├── test_ui_briefing.py            ← Playwright ou requests simples
    └── test_video_gerado.py           ← Verifica MP4 válido no final
```

### Template de teste unitário
```python
# tests/unit/test_script_generator.py
import pytest
from unittest.mock import MagicMock, patch
from app.pipelines.script_generator import ScriptGenerator

class TestScriptGenerator:
    
    def setup_method(self):
        self.logger = MagicMock()
        self.gen = ScriptGenerator(self.logger)
    
    def test_gerar_roteiro_briefing_valido(self):
        """Deve gerar roteiro com 3-5 cenas para briefing válido"""
        roteiro = self.gen.gerar("Vender boneco Medabee 3D para colecionadores")
        assert roteiro is not None
        assert len(roteiro.cenas) >= 3
        assert len(roteiro.cenas) <= 5
        assert roteiro.titulo != ""
    
    def test_rejeitar_briefing_vazio(self):
        """Deve lançar ValueError para briefing vazio"""
        with pytest.raises(ValueError, match="Briefing não pode estar vazio"):
            self.gen.gerar("")
    
    def test_rejeitar_briefing_muito_curto(self):
        """Briefing com menos de 20 chars deve ser rejeitado"""
        with pytest.raises(ValueError):
            self.gen.gerar("vender algo")
    
    def test_roteiro_em_portugues(self):
        """Roteiro deve estar em PT-BR"""
        roteiro = self.gen.gerar("Quero anunciar meu serviço de limpeza residencial")
        # Verificar palavras comuns em PT-BR
        texto = " ".join([c.descricao for c in roteiro.cenas]).lower()
        assert any(w in texto for w in ["o", "a", "de", "com", "para"])
    
    @patch('app.pipelines.script_generator.OllamaAdapter')
    def test_fallback_sem_ollama(self, mock_ollama):
        """Deve gerar roteiro básico mesmo sem Ollama disponível"""
        mock_ollama.side_effect = Exception("Ollama não disponível")
        roteiro = self.gen.gerar("Serviço de manutenção de ar condicionado")
        # Deve retornar template básico, não crashar
        assert roteiro is not None
```

### Script de testes completo (scripts/run_tests.bat)
```bat
@echo off
echo ============================================
echo galFlowAI — Suite de Testes Completa
echo ============================================

echo.
echo [1/4] Testes unitarios Python...
python -m pytest tests/unit/ -v --tb=short --cov=app --cov-report=term-missing
if errorlevel 1 (
    echo FALHA nos testes unitarios
    exit /b 1
)

echo.
echo [2/4] Testes de integracao Python...
python -m pytest tests/integration/ -v --tb=short
if errorlevel 1 (
    echo FALHA nos testes de integracao
    exit /b 1
)

echo.
echo [3/4] Testes Go...
go test ./... -v -cover
if errorlevel 1 (
    echo FALHA nos testes Go
    exit /b 1
)

echo.
echo [4/4] Relatorio de cobertura...
python -m pytest tests/ --cov=app --cov-report=html:coverage_html
echo Relatorio gerado em: coverage_html/index.html

echo.
echo ============================================
echo TODOS OS TESTES PASSARAM
echo ============================================
```

---

## ETAPA 6 — SISTEMA DE LOGS ROBUSTO

### Tarefa 6.1 — logging_config.py melhorado
```python
# app/logging_config.py — MELHORAR

import logging
import sys
from pathlib import Path
from datetime import datetime

NIVEIS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "aviso": logging.WARNING,
    "erro": logging.ERROR,
}

def configurar_logs(nivel: str = "info", projeto_id: str = None) -> logging.Logger:
    """
    Configura logs em 3 destinos:
    1. Console: colorido, humano legível, em PT-BR
    2. Arquivo geral: K:/AI_.../logs/galflowai.log
    3. Arquivo do projeto: K:/AI_.../projects/<id>/logs/pipeline.log
    """
    
    formato_console = "%(asctime)s [%(levelname)s] %(message)s"
    formato_arquivo = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    logger = logging.getLogger("galFlowAI")
    logger.setLevel(NIVEIS.get(nivel, logging.INFO))
    
    # Handler console com cores
    console = ColorConsoleHandler()
    console.setFormatter(logging.Formatter(formato_console, datefmt="%H:%M:%S"))
    logger.addHandler(console)
    
    # Handler arquivo geral (rotação por tamanho)
    from logging.handlers import RotatingFileHandler
    log_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo_geral = RotatingFileHandler(
        log_dir / "galflowai.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    arquivo_geral.setFormatter(logging.Formatter(formato_arquivo))
    logger.addHandler(arquivo_geral)
    
    # Handler arquivo do projeto (se fornecido)
    if projeto_id:
        proj_log_dir = Path(f"K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects/{projeto_id}/logs")
        proj_log_dir.mkdir(parents=True, exist_ok=True)
        arquivo_proj = logging.FileHandler(proj_log_dir / "pipeline.log", encoding="utf-8")
        arquivo_proj.setFormatter(logging.Formatter(formato_arquivo))
        logger.addHandler(arquivo_proj)
    
    return logger


class ColorConsoleHandler(logging.StreamHandler):
    """Handler com cores ANSI para o console Windows"""
    CORES = {
        logging.DEBUG:   "\033[36m",   # Ciano
        logging.INFO:    "\033[32m",   # Verde
        logging.WARNING: "\033[33m",   # Amarelo
        logging.ERROR:   "\033[31m",   # Vermelho
    }
    RESET = "\033[0m"
    
    def emit(self, record):
        cor = self.CORES.get(record.levelno, "")
        record.levelname = self._traduzir_nivel(record.levelname)
        record.msg = f"{cor}{record.msg}{self.RESET}"
        super().emit(record)
    
    def _traduzir_nivel(self, nivel: str) -> str:
        return {"DEBUG": "DEBUG", "INFO": "INFO", 
                "WARNING": "AVISO", "ERROR": "ERRO"}.get(nivel, nivel)
```

### Tarefa 6.2 — Eventos de log para o frontend
```python
# Cada log importante deve emitir evento WebSocket:
# { "tipo": "log", "nivel": "info", "msg": "Roteiro gerado com 4 cenas", "ts": "14:23:01" }
# O frontend exibe no painel de log em tempo real
```

---

## ETAPA 7 — MELHORIAS DE UX/QUALIDADE

### Tarefa 7.1 — Persistência de preferências
```javascript
// frontend/static/js/app.js
const PREFS_KEY = "galflowai_prefs";

const prefsDefault = {
  voz: "feminino",
  velocidade: 1.0,
  duracao: 30,
  estilo: "animado",
  nivel_log: "info",
  tema: "dark",
  ultimo_briefing: "",
};

function salvarPrefs(prefs) {
  localStorage.setItem(PREFS_KEY, JSON.stringify({...prefsDefault, ...prefs}));
}

function carregarPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY)) || prefsDefault;
  } catch {
    return prefsDefault;
  }
}
```

### Tarefa 7.2 — Notificações toast
```javascript
function toast(msg, tipo = "info", duracao = 4000) {
  // Tipos: "info" | "sucesso" | "aviso" | "erro"
  const el = document.createElement("div");
  el.className = `toast toast-${tipo}`;
  el.textContent = msg;
  document.getElementById("toast-container").appendChild(el);
  setTimeout(() => el.remove(), duracao);
}

// Exemplos de uso:
// toast("Roteiro gerado com 4 cenas!", "sucesso")
// toast("VRAM abaixo de 1GB — performance reduzida", "aviso")
// toast("Erro ao iniciar WanGP — usando FFmpeg", "erro")
```

### Tarefa 7.3 — Estado de carregamento (skeleton)
```css
/* Mostrar skeleton loading enquanto dados carregam */
.skeleton {
  background: linear-gradient(90deg, #1a1a1a 25%, #242424 50%, #1a1a1a 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Tarefa 7.4 — Drag and drop nas cenas
```javascript
// Reordenar cenas do roteiro arrastando
// Usar API nativa HTML5 drag-and-drop (sem libs externas)
// Atualizar ordem no estado interno e mostrar preview reordenado
```

---

## ETAPA 8 — PIPELINE DE PR E COMMITS

### Estrutura de PRs (uma PR por etapa)

```
PR #1 — feat: estrutura Go (cmd/, core/) + build script
  - Arquivos: cmd/, core/, go.mod, go.sum, scripts/build_go.bat
  - Testes: go test ./... passando
  - Sem quebrar Python existente

PR #2 — feat: frontend premium (substituir Gradio)
  - Arquivos: frontend/, app/main.py atualizado (servir estático)
  - Testes: UI carrega, API responde, WebSocket conecta
  - Screenshots antes/depois no PR

PR #3 — feat: integração WanGP 1.3B real
  - Arquivos: app/adapters/wangp_adapter.py reescrito
  - Testes: test_wangp_adapter.py cobrindo fallback
  - Documentar: como verificar se WanGP está instalado

PR #4 — feat: TTS narração offline (masculino/feminino)
  - Arquivos: app/adapters/tts_adapter.py reescrito, voice_pipeline.py
  - Testes: test_tts_adapter.py com mocks de kokoro e pyttsx3
  - Demo: audio de preview funcionando

PR #5 — feat: testes 100% + CI local
  - Arquivos: tests/ completo, scripts/run_tests.bat
  - Testes: cobertura >= 80% Python, >= 80% Go
  - README atualizado com como rodar testes

PR #6 — feat: logs avançados + monitoramento
  - Arquivos: app/logging_config.py reescrito
  - Testes: logs aparecem no frontend via WebSocket
  - Validar: log rotacionado, projeto tem log próprio

PR #7 — polish: UX, preferências, notificações, drag-and-drop
  - Arquivos: frontend/static/js/app.js, preferências salvas
  - Testes: e2e básico com requests
  - Screenshots da UI final
```

### Template de commit
```
tipo(escopo): descrição em português

Exemplos válidos:
  feat(wangp): integrar adaptador real com fallback para FFmpeg
  fix(tts): corrigir seleção de voz feminina no pyttsx3
  test(pipeline): adicionar testes de integração end-to-end
  refactor(queue): migrar fila para BoltDB persistente
  docs(readme): atualizar instruções de instalação do Go
  style(frontend): aplicar design system premium dark mode
  perf(go): paralelizar renderização de múltiplas cenas

Regras:
- Máximo 72 caracteres na primeira linha
- Corpo do commit em PT-BR
- Referenciar issue/tarefa se houver: "Closes #12"
```

---

## ETAPA 9 — README.md ATUALIZADO

O README deve incluir:

```markdown
## Requisitos

### Python
- Python 3.10+ (ambiente K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio)
- Pacotes: gradio, ffmpeg-python, pyttsx3, kokoro (opcional)

### Go
- Go 1.21+ (https://go.dev/dl/)
- Compilar: scripts\build_go.bat

### GPU
- NVIDIA GTX 1660 Super ou superior
- 6 GB VRAM mínimo
- CUDA Toolkit compatível com WanGP

### Disco
- Drive K: com 100 GB livres

## Como iniciar

# Opção 1: Executável Go (recomendado — mais rápido)
galflowai.exe

# Opção 2: Python direto
scripts\start_app.bat

## Como rodar os testes

scripts\run_tests.bat

## Vozes disponíveis

O sistema detecta automaticamente as vozes instaladas no Windows.
Para instalar vozes PT-BR adicionais:
Configurações → Hora e idioma → Fala → Gerenciar vozes
```

---

## CHECKLIST FINAL DE QUALIDADE

Antes de abrir cada PR, verificar:

```
[ ] Todos os logs em português brasileiro
[ ] Nenhum arquivo salvo fora de K:
[ ] Nenhuma chamada a API paga ou externa
[ ] Fallback gracioso em todos os adapters (nunca crashar sem resultado)
[ ] Testes unitários escritos para cada nova função
[ ] Cobertura >= 80% no módulo alterado
[ ] UI carrega sem erros no console do browser
[ ] Barra de progresso reflete progresso real (não finge)
[ ] Log de erro claro e acionável quando algo falha
[ ] go test ./... passando (se alterou código Go)
[ ] pytest tests/ passando (se alterou código Python)
[ ] WanGP bloqueado em modo seguro quando VRAM < 4GB
[ ] README atualizado com mudanças relevantes
```

---

## ORDEM DE EXECUÇÃO PARA O OpenCode Hy3

```
1. Ler e entender TODO este documento antes de escrever qualquer código
2. Começar pela Etapa 1 (Go) — base do servidor
3. Seguir para Etapa 2 (Frontend) — conectar ao servidor Go
4. Etapa 3 (WanGP) — ativar geração real de vídeo
5. Etapa 4 (TTS) — adicionar narração
6. Etapa 5 (Testes) — cobrir tudo
7. Etapas 6-7 (Logs + UX polish) — refinamento
8. Etapa 8 (PRs) — commitar em ordem, um PR por etapa
9. Etapa 9 (README) — documentar ao final

A cada etapa: rodar os testes, commitar, abrir PR.
Não avançar para próxima etapa com testes falhando.
```

---

*galFlowAI — Crie comerciais profissionais sem sair do seu PC, sem gastar nada.*
*Versão deste prompt: 2.0 | Gerado em: 2026-05-02*
