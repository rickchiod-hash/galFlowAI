import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock
from app.services.tts_service import TTSService


class TestTTSService:
    def test_init_unavailable(self):
        with patch("app.services.tts_service.TTSService._check_available", return_value=False):
            tts = TTSService()
        assert tts.is_available() is False
        assert tts.engine is None

    def test_init_available(self):
        with (
            patch.object(TTSService, "_check_available", return_value=True),
            patch.object(TTSService, "_init_engine"),
        ):
            tts = TTSService()
        assert tts.available is True

    def test_check_available_true(self):
        with patch("builtins.__import__") as mock_import:
            tts = TTSService.__new__(TTSService)
            result = tts._check_available()
        assert result is True

    def test_check_available_false(self):
        tts = TTSService.__new__(TTSService)
        result = tts._check_available()
        assert result is False

    def test_init_calls_init_engine(self):
        with (
            patch("app.services.tts_service.TTSService._check_available", return_value=True),
            patch("app.services.tts_service.TTSService._init_engine") as mock_init,
        ):
            tts = TTSService()
        mock_init.assert_called_once()
        assert tts.available is True

    def test_is_available_true(self):
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = MagicMock()
        assert tts.is_available() is True

    def test_is_available_false_no_engine(self):
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = None
        assert tts.is_available() is False

    def test_generate_audio_unavailable(self):
        tts = TTSService.__new__(TTSService)
        tts.available = False
        tts.engine = None
        result = tts.generate_audio("text", "/tmp/out.wav")
        assert result["success"] is False
        assert "não disponível" in result["error"]
        assert result["fallback_suggested"] is True

    def test_generate_audio_success(self):
        mock_engine = MagicMock()
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        with (
            patch.object(Path, "mkdir"),
            patch.object(Path, "exists", return_value=True),
        ):
            result = tts.generate_audio("Texto de teste", "/tmp/out.wav")
        assert result["success"] is True
        assert "pyttsx3" in result["provider"]
        mock_engine.save_to_file.assert_called_once()
        mock_engine.runAndWait.assert_called_once()

    def test_generate_audio_file_not_created(self):
        mock_engine = MagicMock()
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        with (
            patch.object(Path, "mkdir"),
            patch.object(Path, "exists", return_value=False),
        ):
            result = tts.generate_audio("Texto", "/tmp/out.wav")
        assert result["success"] is False
        assert "não foi criado" in result["error"]

    def test_generate_audio_exception(self):
        mock_engine = MagicMock()
        mock_engine.save_to_file.side_effect = RuntimeError("no codec")
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        result = tts.generate_audio("Texto", "/tmp/out.wav")
        assert result["success"] is False
        assert "no codec" in result["error"]

    def test_generate_audio_with_voice(self):
        mock_engine = MagicMock()
        maria = MagicMock()
        maria.name = "Microsoft Maria"
        maria.id = "maria_id"
        david = MagicMock()
        david.name = "Microsoft David"
        david.id = "david_id"
        mock_engine.getProperty.return_value = [maria, david]
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        with (
            patch.object(Path, "mkdir"),
            patch.object(Path, "exists", return_value=True),
        ):
            result = tts.generate_audio("Texto", "/tmp/out.wav", voice="maria")
        assert result["success"] is True
        mock_engine.setProperty.assert_any_call("voice", "maria_id")

    def test_get_available_voices_unavailable(self):
        tts = TTSService.__new__(TTSService)
        tts.available = False
        tts.engine = None
        voices = tts.get_available_voices()
        assert voices == []

    def test_get_available_voices_success(self):
        mock_engine = MagicMock()
        voice = MagicMock()
        voice.id = "v1"
        voice.name = "Voice1"
        voice.languages = ["pt-BR"]
        mock_engine.getProperty.return_value = [voice]
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        voices = tts.get_available_voices()
        assert len(voices) == 1
        assert voices[0]["id"] == "v1"

    def test_get_available_voices_exception(self):
        mock_engine = MagicMock()
        mock_engine.getProperty.side_effect = ValueError("bad prop")
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = mock_engine
        voices = tts.get_available_voices()
        assert voices == []

    def test_get_status_available(self):
        tts = TTSService.__new__(TTSService)
        tts.available = True
        tts.engine = MagicMock()
        with patch.object(TTSService, "get_available_voices", return_value=[{"id": "v1"}]):
            status = tts.get_status()
        assert status["available"] is True
        assert status["voices_count"] == 1

    def test_get_status_unavailable(self):
        tts = TTSService.__new__(TTSService)
        tts.available = False
        tts.engine = None
        status = tts.get_status()
        assert status["available"] is False
        assert status["voices_count"] == 0
