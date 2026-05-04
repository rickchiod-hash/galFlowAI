#!/usr/bin/env python
"""Corrige erros de sintaxe no api.py (ponto e vírgula em dicionários)"""

import sys
from pathlib import Path

def fix_api_syntax():
    api_path = Path("app/api.py")
    
    if not api_path.exists():
        print(f"Erro: {api_path} não encontrado")
        return False
    
    # Ler arquivo
    content = api_path.read_text(encoding="utf-8")
    
    # Corrigir: trocar ponto e vírgula por vírgula em dictionaries
    # Padrão: { "key": value; "key2": value2 } -> { "key": value, "key2": value2 }
    
    lines = content.split('\n')
    fixed_lines = []
    errors_fixed = 0
    
    for line in lines:
        original = line
        # Trocar ; por , dentro de dictionaries (simplificado)
        if ';' in line and ('{' in line or '}' in line or 'return {' in line or 'send_json({' in line):
            # Substituir ; por , quando estiver em contexto de dicionário
            line = line.replace('; ', ', ')
            line = line.replace(';}', '}')
            if line != original:
                errors_fixed += 1
        fixed_lines.append(line)
    
    # Salvar arquivo corrigido
    fixed_content = '\n'.join(fixed_lines)
    api_path.write_text(fixed_content, encoding="utf-8")
    
    print(f"Corrigidos {errors_fixed} erros de sintaxe em {api_path}")
    return True


def check_syntax():
    """Verifica sintaxe dos arquivos Python"""
    import py_compile
    
    files = ["app/api.py", "app/main.py"]
    all_ok = True
    
    for f in files:
        try:
            py_compile.compile(f, doraise=True)
            print(f"✓ {f} - sintaxe OK")
        except py_compile.PyCompileError as e:
            print(f"✗ {f} - erro: {e}")
            all_ok = False
    
    return all_ok


if __name__ == "__main__":
    print("=" * 60)
    print("   CORRIGINDO ERROS DE SINTAXE")
    print("=" * 60)
    print()
    
    print("[1/2] Corrigindo api.py...")
    fix_api_syntax()
    
    print("[2/2] Verificando sintaxe...")
    if check_syntax():
        print()
        print("✓ Todos os arquivos estão com sintaxe correta!")
        sys.exit(0)
    else:
        print()
        print("✗ Ainda existem erros de sintaxe")
        sys.exit(1)
