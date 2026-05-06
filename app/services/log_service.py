"""
LogService - Serviço síncrono para leitura, resumo e formatação de logs.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Caminho base dos logs
LOG_DIR = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/logs")
MAX_LINES = 500  # Limite para não travar UI

def _get_log_file():
    """Retorna caminho do arquivo de log principal."""
    return LOG_DIR / "galflowai.log"


def _read_last_lines(filepath: Path, n: int = 200) -> List[str]:
    """
    Lê as últimas N linhas de um arquivo de forma eficiente.
    Não carrega arquivo inteiro na memória.
    """
    if not filepath.exists():
        return ["Arquivo de log ainda não existe."]

    try:
        # Método eficiente para arquivos grandes
        with open(filepath, 'rb') as f:
            f.seek(0, os.SEEK_END)
            position = f.tell()
            lines = []
            buffer = bytearray()

            while position >= 0 and len(lines) < n:
                f.seek(position)
                chunk = f.read(1)
                if chunk == b'\n' and buffer:
                    lines.append(buffer.decode('utf-8', errors='ignore').strip())
                    buffer = bytearray()
                else:
                    buffer.extend(chunk)
                position -= 1

            if buffer:
                lines.append(buffer.decode('utf-8', errors='ignore').strip())

            return list(reversed(lines))
    except Exception as e:
        return [f"Erro ao ler log: {str(e)}"]


def get_recent_logs(level: Optional[str] = None, search: Optional[str] = None, limit: int = 200) -> Dict[str, Any]:
    """
    Retorna logs recentes com filtros.
    SEMPRE síncrono conforme instruções.
    """
    log_file = _get_log_file()

    if not log_file.exists():
        return {
            "logs": [],
            "total": 0,
            "message": "Arquivo de log ainda não existe. Gere um roteiro para criar logs."
        }

    lines = _read_last_lines(log_file, max(limit, MAX_LINES))

    results = []
    for line in lines:
        # Filtrar por nível (DEBUG não deve aparecer na UI)
        line_lower = line.lower()

        # Remover DEBUG da UI
        if 'debug' in line_lower:
            continue

        # Filtrar por nível se especificado
        if level:
            level_lower = level.lower()
            if level_lower == "info" and 'info' not in line_lower:
                continue
            elif level_lower == "warn" and 'warn' not in line_lower and 'warning' not in line_lower:
                continue
            elif level_lower == "error" and 'error' not in line_lower:
                continue

        # Busca por texto
        if search:
            if search.lower() not in line_lower:
                continue

        # Parse da linha (formato: timestamp | level | module | message)
        parts = line.split(' | ', 3)
        if len(parts) >= 3:
            results.append({
                "horario": parts[0].strip() if len(parts) > 0 else "",
                "nivel": _normalize_level(parts[1].strip()) if len(parts) > 1 else "UNKNOWN",
                "modulo": parts[2].strip() if len(parts) > 2 else "",
                "projeto": "",  # Extrair de ' | ' se existir
                "job": "",
                "mensagem": parts[3].strip() if len(parts) > 3 else line,
                "sugestao": _get_suggestion(line)
            })
        else:
            results.append({
                "horario": "",
                "nivel": "UNKNOWN",
                "modulo": "",
                "projeto": "",
                "job": "",
                "mensagem": line,
                "sugestao": ""
            })

    return {
        "logs": results[:limit],
        "total": len(results),
        "message": f"{len(results)} logs encontrados."
    }


def get_log_summary() -> Dict[str, Any]:
    """Retorna resumo dos logs."""
    log_file = _get_log_file()

    if not log_file.exists():
        return {
            "total_info": 0,
            "total_warn": 0,
            "total_error": 0,
            "last_error": "",
            "last_update": "",
            "log_file": str(log_file),
            "message": "Arquivo de log ainda não existe."
        }

    try:
        content = log_file.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        total_info = sum(1 for l in lines if ' | INFO | ' in l)
        total_warn = sum(1 for l in lines if ' | WARNING | ' in l or ' | WARN | ' in l)
        total_error = sum(1 for l in lines if ' | ERROR | ' in l)

        # Último erro
        error_lines = [l for l in lines if ' | ERROR | ' in l]
        last_error = error_lines[-1] if error_lines else ""

        # Última atualização
        last_update = datetime.now().strftime("%H:%M:%S")

        return {
            "total_info": total_info,
            "total_warn": total_warn,
            "total_error": total_error,
            "last_error": last_error[:200] if last_error else "",
            "last_update": last_update,
            "log_file": str(log_file),
            "message": "Resumo atualizado."
        }
    except Exception as e:
        return {
            "total_info": 0,
            "total_warn": 0,
            "total_error": 0,
            "last_error": "",
            "last_update": "",
            "log_file": str(log_file),
            "message": f"Erro ao ler resumo: {str(e)}"
        }


def get_last_error() -> Dict[str, Any]:
    """Retorna último erro encontrado."""
    log_file = _get_log_file()

    if not log_file.exists():
        return {"error": "", "message": "Arquivo de log ainda não existe."}

    try:
        lines = _read_last_lines(log_file, 500)
        for line in reversed(lines):
            if 'error' in line.lower():
                return {"error": line, "message": "Último erro encontrado."}
        return {"error": "", "message": "Nenhum erro encontrado nos logs recentes."}
    except Exception as e:
        return {"error": "", "message": f"Erro: {str(e)}"}


def format_logs_for_table(logs: List[Dict]) -> List[Dict]:
    """Formata logs para exibição em tabela."""
    return logs  # Já está no formato correto


def format_logs_for_console(logs: List[Dict]) -> str:
    """Formata logs para exibição em console bruto."""
    if not logs:
        return "Nenhum log para exibir."

    output = ""
    for log in logs[:50]:  # Limitar a 50 para não travar
        nivel = log.get("nivel", "UNKNOWN")
        msg = log.get("mensagem", "")
        horario = log.get("horario", "")
        output += f"{horario} [{nivel}] {msg}\n"

    return output


def copy_diagnostic_bundle() -> str:
    """Gera texto de diagnóstico copiável."""
    try:
        import sys
        import subprocess

        bundle = []
        bundle.append("=== DIAGNÓSTICO FLOWFORGEAI ===")
        bundle.append(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        # Commit atual
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True, text=True, timeout=5,
                cwd="K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta"
            )
            bundle.append(f"Commit atual: {result.stdout.strip()}")
        except:
            bundle.append("Commit atual: não disponível")

        bundle.append(f"Python: {sys.version.split()[0]}")
        bundle.append("Porta Gradio: 127.0.0.1:7860")
        bundle.append("Porta FastAPI: 127.0.0.1:8000")

        # Logs recentes WARN/ERROR
        recent = get_recent_logs(limit=20)
        errors = [l for l in recent.get("logs", []) if l.get("nivel") in ["ERROR", "WARN"]]
        if errors:
            bundle.append("\nÚltimos erros/warnings:")
            for e in errors[:10]:
                bundle.append(f"  {e.get('horario')} [{e.get('nivel')}] {e.get('mensagem')[:100]}")

        # Status providers
        bundle.append("\nStatus dos providers:")
        bundle.append("  TemplateProvider: Sempre disponível")

        try:
            from app.adapters.llm import ProviderRouter
            router = ProviderRouter()
            available = router.detect_available()
            for k, v in available.items():
                bundle.append(f"  {k}: {'✓' if v else '✗'}")
        except Exception as e:
            bundle.append(f"  Erro ao verificar providers: {str(e)}")

        # Status FFmpeg
        bundle.append("\nStatus FFmpeg:")
        try:
            from app.adapters.ffmpeg_adapter import FFmpegAdapter
            adapter = FFmpegAdapter()
            status = adapter.get_status()
            bundle.append(f"  Disponível: {status.get('available', False)}")
            bundle.append(f"  Caminho: {status.get('path', 'N/A')}")
        except Exception as e:
            bundle.append(f"  Erro: {str(e)}")

        bundle.append(f"\nCaminho dos logs: {LOG_DIR}")
        bundle.append("\nSugestão: Verifique se Gradio subiu em http://127.0.0.1:7860")
        bundle.append("Se houver erro, consulte docs/TROUBLESHOOTING.md")

        return "\n".join(bundle)
    except Exception as e:
        return f"Erro ao gerar diagnóstico: {str(e)}"


def open_logs_folder():
    """Abre pasta de logs no explorador (Windows)."""
    try:
        import subprocess
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.Popen(f'explorer "{LOG_DIR}"')
        return {"ok": True, "message": "Pasta de logs aberta."}
    except Exception as e:
        return {"ok": False, "message": f"Erro: {str(e)}"}


def _normalize_level(level_str: str) -> str:
    """Normaliza nível para UI (DEBUG não aparece)."""
    level_lower = level_str.lower()
    if 'debug' in level_lower:
        return "DEBUG"  # Não deve aparecer na UI
    elif 'info' in level_lower:
        return "INFO"
    elif 'warn' in level_lower or 'aviso' in level_lower or 'warning' in level_lower:
        return "WARN"
    elif 'error' in level_lower or 'erro' in level_lower:
        return "ERROR"
    else:
        return level_str.upper()


def _get_suggestion(log_line: str) -> str:
    """Retorna sugestão baseada no erro."""
    line_lower = log_line.lower()

    if 'ffmpeg' in line_lower and 'não' in line_lower:
        return "Instale FFmpeg ou use WAN GP. Veja docs/TROUBLESHOOTING.md"
    elif 'permission' in line_lower:
        return "Verifique permissões de arquivo/pasta"
    elif 'module' in line_lower and 'not found' in line_lower:
        return "Módulo não encontrado. Verifique imports e ambiente Python"
    elif 'connection' in line_lower or 'refused' in line_lower:
        return "Verifique se o servidor está rodando na porta correta"
    elif 'template' in line_lower:
        return "TemplateProvider é fallback obrigatório"
    else:
        return ""
