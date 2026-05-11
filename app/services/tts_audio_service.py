"""TTS Audio Service (AUD-701).

Gera audio por cena usando AudioPlan como entrada.
Fallback silencioso: se TTS falhar para uma cena,
a cena continua sem audio — nao bloqueia o pipeline.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.domain.audio_plan import AudioPlan

logger = logging.getLogger(__name__)


class TTSAudioService:
    """Servico que gera audio por cena a partir de um AudioPlan.

    Para cada entrada de narracao no plano, gera um arquivo WAV
    no diretorio de saida. Falhas sao registradas em log mas
    nao interrompem o processo.
    """

    def __init__(self, tts_adapter: Any):
        self.tts_adapter = tts_adapter

    def generate_scene_audio(
        self,
        plan: AudioPlan,
        output_dir: str,
    ) -> List[Dict[str, Any]]:
        """Gera arquivos de audio para cada cena do plano.

        Args:
            plan: AudioPlan com as entradas de narracao.
            output_dir: Diretorio onde os arquivos WAV serao salvos.

        Returns:
            Lista de dicts com resultado por cena:
            {scene_number, audio_path, success, error (se falhou)}.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        results: List[Dict[str, Any]] = []

        for entry in plan.narrations:
            scene_num = entry.scene_number
            wav_name = f"scene_{scene_num:03d}.wav"
            wav_path = str(out / wav_name)

            try:
                result = self.tts_adapter.generate_audio(
                    text=entry.narration_text,
                    output_path=wav_path,
                    voice=entry.tts_voice if entry.tts_voice != "default" else None,
                    speed=1.0,
                    language=entry.language,
                )

                if result.get("success"):
                    logger.info(
                        "Audio gerado para cena %d: %s (engine: %s)",
                        scene_num, wav_name, result.get("engine", "?"),
                    )
                    results.append({
                        "scene_number": scene_num,
                        "audio_path": wav_path,
                        "success": True,
                        "engine": result.get("engine", "?"),
                    })
                else:
                    logger.warning(
                        "Falha ao gerar audio para cena %d: %s",
                        scene_num, result.get("error", "erro desconhecido"),
                    )
                    results.append({
                        "scene_number": scene_num,
                        "audio_path": None,
                        "success": False,
                        "error": result.get("error", "erro desconhecido"),
                    })

            except Exception as exc:
                logger.error(
                    "Excecao ao gerar audio para cena %d: %s",
                    scene_num, exc,
                )
                results.append({
                    "scene_number": scene_num,
                    "audio_path": None,
                    "success": False,
                    "error": str(exc),
                })

        return results

    def get_audio_map(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[int, Optional[str]]:
        """Converte lista de resultados em mapa cena -> caminho.

        Uteis para pipelines que precisam de lookup rapido
        de qual audio pertence a qual cena.
        """
        return {
            r["scene_number"]: r.get("audio_path")
            for r in results
        }
