"""SRT Service (AUD-702).

Gera arquivos SRT (SubRip Subtitle) a partir de um AudioPlan.
As legendas sao derivadas das entradas de narracao com timing
baseado na duracao estimada de cada cena.

SRT e sempre derivado do AudioPlan — nunca gerado
independentemente (regra de preservacao #3).
"""

import logging
from pathlib import Path
from typing import Optional

from app.domain.audio_plan import AudioPlan

logger = logging.getLogger(__name__)

# Caracteres por segundo para estimativa de duracao
_CHARS_PER_SECOND = 15.0
_MIN_DURATION_SECONDS = 2.0


def _estimate_duration(text: str) -> float:
    """Estima duracao de narracao baseada no tamanho do texto."""
    return max(_MIN_DURATION_SECONDS, len(text) / _CHARS_PER_SECOND)


def _format_srt_timestamp(total_seconds: float) -> str:
    """Converte segundos para formato SRT: HH:MM:SS,mmm."""
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    millis = int((total_seconds - int(total_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


class SRTService:
    """Servico que gera legendas SRT a partir de um AudioPlan."""

    @staticmethod
    def estimate_duration(text: str) -> float:
        """Estima duracao de narracao baseada no tamanho do texto.
        
        Usado quando NarrationEntry.duration_seconds e 0.
        """
        return _estimate_duration(text)

    def generate_srt_content(self, plan: AudioPlan) -> str:
        """Gera conteudo SRT como string a partir do plano.
        
        Cada cena vira um subtitle entry com timing sequencial.
        Se duration_seconds == 0, estima pela contagem de caracteres.
        
        Args:
            plan: AudioPlan com entradas de narracao.
            
        Returns:
            String no formato SRT.
        """
        lines = []
        current_time = 0.0

        sorted_narrations = sorted(
            plan.narrations, key=lambda n: n.scene_number
        )

        for idx, entry in enumerate(sorted_narrations, 1):
            duration = (
                entry.duration_seconds
                if entry.duration_seconds > 0
                else _estimate_duration(entry.narration_text)
            )
            start_time = current_time
            end_time = current_time + duration
            current_time = end_time

            start_ts = _format_srt_timestamp(start_time)
            end_ts = _format_srt_timestamp(end_time)

            lines.append(str(idx))
            lines.append(f"{start_ts} --> {end_ts}")
            lines.append(entry.narration_text)
            lines.append("")

        return "\n".join(lines)

    def generate_srt_file(
        self,
        plan: AudioPlan,
        output_path: str,
    ) -> str:
        """Gera arquivo SRT a partir do AudioPlan.
        
        Args:
            plan: AudioPlan com entradas de narracao.
            output_path: Caminho para salvar o arquivo .srt.
            
        Returns:
            Conteudo SRT gerado.
        """
        content = self.generate_srt_content(plan)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        logger.info("SRT gerado: %s (%d entradas)", output_path, len(plan.narrations))
        return content
