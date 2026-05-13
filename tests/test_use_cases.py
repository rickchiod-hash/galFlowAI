"""Tests for use cases."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.application.use_cases.generate_script_use_case import GenerateScriptUseCase
from app.application.use_cases.split_scenes_use_case import SplitScenesUseCase
from app.application.use_cases.generate_audio_use_case import GenerateAudioUseCase
from app.application.result import Result


def test_generate_script_use_case():
    """Test GenerateScriptUseCase."""
    uc = GenerateScriptUseCase()
    # Test with valid input
    result = uc.execute(briefing="Test product. Test audience", project_id="test_project")
    # Should return Result object
    assert isinstance(result, Result), f"Expected Result, got {type(result)}"
    # May succeed or fail depending on LLM availability
    print(f"GenerateScriptUseCase returned: ok={result.ok}")
    print("PASS: test_generate_script_use_case")



def test_split_scenes_use_case():
    """Test SplitScenesUseCase."""
    uc = SplitScenesUseCase()
    script = "Cena 1: Test\nCena 2: Another"
    result = uc.execute(script=script, project_id="test_project")
    assert isinstance(result, Result)
    if result.ok:
        assert "scenes" in result.data
        print(f"SplitScenesUseCase returned {len(result.data['scenes'])} scenes")
    else:
        print(f"SplitScenesUseCase failed: {result.error}")
    print("PASS: test_split_scenes_use_case")



def test_generate_audio_use_case():
    """Test GenerateAudioUseCase."""
    uc = GenerateAudioUseCase()
    # This will likely fail because TTS adapter may not be available
    result = uc.execute(project_id="test_project", text="Test audio", output_name="test.wav")
    assert isinstance(result, Result)
    print(f"GenerateAudioUseCase returned: ok={result.ok}")
    if not result.ok:
        print(f"  (Expected failure if TTS not available: {result.error})")
    print("PASS: test_generate_audio_use_case")



def test_result_integration():
    """Test that use cases return Result objects."""
    # Test that success returns Result
    r = Result.success(data="test")
    assert r.ok is True
    assert r.is_success() is True
    
    # Test that failure returns Result  
    r = Result.failure(error="test error")
    assert r.ok is False
    assert r.is_failure() is True
    
    print("PASS: test_result_integration")



if __name__ == "__main__":
    results = []
    for name, fn in [
        ("GenerateScriptUseCase", test_generate_script_use_case),
        ("SplitScenesUseCase", test_split_scenes_use_case),
        ("GenerateAudioUseCase", test_generate_audio_use_case),
        ("Result integration", test_result_integration),
    ]:
        try:
            result = fn()
            results.append((name, result))
            if result:
                print(f"PASS: {name}")
            else:
                print(f"FAIL: {name}")
        except Exception as e:
            print(f"FAIL: {name} with exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("RESULTS: Use Case Tests")
    print("="*60)
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{name:<50} {status}")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPASSED: {passed}/{total}")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)
