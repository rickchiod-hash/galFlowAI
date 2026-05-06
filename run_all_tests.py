"""Script para rodar todos os testes do GalFlowAI"""

import sys
import unittest
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))


def run_all_tests():
    """Executa todos os testes unitários"""
    print("=" * 60)
    print("GalFlowAI - Executor de Testes Completo")
    print("=" * 60)
    print()
    
    # Descobre todos os testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona os módulos de teste
    test_modules = [
        'test_all_stories',
        'test_video_service',
        'test_prompt_builder',
        'test_scene_splitter',
        'test_complete_system'
    ]
    
    for module in test_modules:
        try:
            # Tenta importar o módulo
            exec(f"import {module}")
            tests = loader.loadTestsFromName(module)
            suite.addTests(tests)
            print(f"[OK] {module} carregado")
        except ImportError as e:
            print(f"[ERRO] {module} não encontrado: {e}")
        except Exception as e:
            print(f"[ERRO] Erro ao carregar {module}: {e}")
    
    print()
    print("-" * 60)
    print("Executando testes...")
    print("-" * 60)
    print()
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumo
    print()
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    
    if result.failures:
        print()
        print("FALHAS:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print()
        print("ERROS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    print()
    if result.wasSuccessful():
        print("STATUS: TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("STATUS: ALGUNS TESTES FALHARAM")
        return 1


def run_specific_test(test_name):
    """Executa um teste específico"""
    print(f"Executando teste: {test_name}")
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    try:
        exec(f"import {test_name}")
        tests = loader.loadTestsFromName(test_name)
        suite.addTests(tests)
    except ImportError:
        print(f"Erro: Módulo {test_name} não encontrado")
        return 1
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Executor de Testes GalFlowAI")
    parser.add_argument(
        "test",
        nargs="?",
        help="Nome do teste específico (opcional)"
    )
    
    args = parser.parse_args()
    
    if args.test:
        sys.exit(run_specific_test(args.test))
    else:
        sys.exit(run_all_tests())
