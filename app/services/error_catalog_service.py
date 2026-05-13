from app.core.error_codes import ErrorCode
from app.core.app_error import AppError, Severity


_ERROR_DEFINITIONS: dict[str, dict] = {
    ErrorCode.UNKNOWN_ERROR: {
        "message": "Erro desconhecido.",
        "suggestion": "Consulte os logs para mais detalhes.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "general",
    },
    ErrorCode.GRADIO_START_FAILED: {
        "message": "Interface Gradio não iniciou.",
        "suggestion": "Verifique se a porta está livre e se as dependências estão instaladas.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "boot",
    },
    ErrorCode.FASTAPI_UNAVAILABLE: {
        "message": "Servidor FastAPI não está respondendo.",
        "suggestion": "Execute health check em /api/health. Verifique se o servidor está rodando.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "boot",
    },
    ErrorCode.LLM_PROVIDER_UNAVAILABLE: {
        "message": "Provedor LLM indisponível no momento.",
        "suggestion": "O TemplateProvider será usado como fallback. Verifique se o servidor LLM está rodando na porta correta.",
        "severity": Severity.WARN,
        "retryable": True,
        "stage": "script",
    },
    ErrorCode.SCRIPT_VALIDATION_FAILED: {
        "message": "Roteiro não passou na validação.",
        "suggestion": "Revise o roteiro e tente novamente. Certifique-se de que contém ao menos uma cena.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "script",
    },
    ErrorCode.FFMPEG_NOT_FOUND: {
        "message": "FFmpeg não encontrado no sistema.",
        "suggestion": "Instale o FFmpeg ou configure o caminho manualmente nas configurações.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "render",
    },
    ErrorCode.FFMPEG_CONCAT_FAILED: {
        "message": "FFmpeg falhou ao concatenar os vídeos.",
        "suggestion": "Valide o arquivo inputs.txt, verifique os caminhos dos arquivos de vídeo e a flag -safe 0. Confirme que nenhum arquivo está ausente ou corrompido.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "render",
    },
    ErrorCode.WANGP_UNAVAILABLE: {
        "message": "WanGP (geração por IA) indisponível.",
        "suggestion": "O FFmpeg será usado como fallback para gerar um preview. Verifique se o modelo WanGP está baixado e a GPU está disponível.",
        "severity": Severity.WARN,
        "retryable": True,
        "stage": "render",
    },
    ErrorCode.TTS_UNAVAILABLE: {
        "message": "Sistema de áudio TTS indisponível.",
        "suggestion": "O vídeo será gerado sem áudio (fallback para silêncio). Verifique se o TTS está configurado corretamente.",
        "severity": Severity.WARN,
        "retryable": True,
        "stage": "audio",
    },
    ErrorCode.PROJECT_NOT_FOUND: {
        "message": "Projeto não encontrado.",
        "suggestion": "Verifique se o ID do projeto está correto. Crie um novo projeto se necessário.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "project",
    },
    ErrorCode.INVALID_PROJECT_STATE: {
        "message": "Estado do projeto inválido para esta operação.",
        "suggestion": "Complete as etapas anteriores antes de prosseguir. Verifique o fluxo de 6 etapas.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "project",
    },
    ErrorCode.TEMPLATE_PROVIDER_FAILED: {
        "message": "TemplateProvider também falhou.",
        "suggestion": "Erro crítico: nem mesmo o fallback funcionou. Consulte os logs técnicos.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "general",
    },
    ErrorCode.FILE_SYSTEM_ERROR: {
        "message": "Erro de sistema de arquivos.",
        "suggestion": "Verifique permissões de escrita e espaço em disco. Caminhos configurados em K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "general",
    },
    ErrorCode.CONFIG_INVALID: {
        "message": "Configuração inválida.",
        "suggestion": "Revise as configurações do projeto. Verifique se todos os campos obrigatórios estão preenchidos.",
        "severity": Severity.ERROR,
        "retryable": False,
        "stage": "config",
    },
    ErrorCode.BOOT_FAILED: {
        "message": "Falha na inicialização do sistema.",
        "suggestion": "Verifique o log de inicialização. Confirme se todas as dependências estão instaladas.",
        "severity": Severity.ERROR,
        "retryable": True,
        "stage": "boot",
    },
}


class ErrorCatalogService:

    def get_error_definition(self, code: str) -> dict | None:
        return _ERROR_DEFINITIONS.get(code)

    def build_user_message(self, error: AppError) -> str:
        return f"{error.message} {error.suggestion}"

    def build_diagnostic_message(self, error: AppError) -> str:
        parts = [
            f"[{error.severity}] {error.code}",
            f"  Etapa: {error.stage}",
            f"  Mensagem: {error.message}",
            f"  Sugestão: {error.suggestion}",
        ]
        if error.project_id:
            parts.append(f"  Projeto: {error.project_id}")
        if error.job_id:
            parts.append(f"  Job: {error.job_id}")
        if error.provider:
            parts.append(f"  Provider: {error.provider}")
        if error.fallback_used:
            parts.append(f"  Fallback usado: sim")
        parts.append(f"  Retryable: {'sim' if error.retryable else 'nao'}")
        return "\n".join(parts)

    def is_retryable(self, code: str) -> bool:
        definition = _ERROR_DEFINITIONS.get(code)
        if definition is None:
            return False
        return definition["retryable"]

    def get_suggestion(self, code: str) -> str:
        definition = _ERROR_DEFINITIONS.get(code)
        if definition is None:
            return "Consulte os logs para mais detalhes."
        return definition["suggestion"]
