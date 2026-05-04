#!/usr/bin/env python
"""Corrige erros de sintaxe no api.py - remove semicolons onde deveria haver commas"""

import re

def fix_api_syntax():
    api_path = "app/api.py"
    
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Corrigir logging: "text: %s"; e) -> "text: %s", e)
    content = re.sub(r'(".*?%s")\s*;\s*(\w+)\)', r'\1, \2)', content)
    
    # 2. Corrigir type hints: Dict[str; Any] -> Dict[str, Any]
    content = re.sub(r'Dict\[(\w+)\s*;\s*(\w+)\]', r'Dict[\1, \2]', content)
    content = re.sub(r'List\[(\w+)\s*;\s*(\w+)\]', r'List[\1, \2]', content)
    
    # 3. Corrigir dictionaries: {"key": value; "key2": value2} -> {"key": value, "key2": value2}
    # Padrão mais simples: trocar ; por , quando entre aspas/chaves
    content = re.sub(r';\s*"', r', "', content)
    content = re.sub(r';\s*\}', r', }', content)
    
    # 4. Corrigir return {"job_id": job_id; "progress": 0; "status": "pending"}
    # Substituir ; por , dentro de dicionários
    def fix_dict_commas(match):
        d = match.group(0)
        # Troca ; por , apenas dentro do dicionário
        d = re.sub(r';\s*(?=["\w{])', r', ', d)
        return d
    
    # Aplica correção em dicionários que têm ;
    content = re.sub(r'\{[^}]*;[^}]*\}', fix_dict_commas, content, flags=re.DOTALL)
    
    # 5. Corrigir especificamente os returns problemáticos
    content = content.replace('"job_id": job_id; "progress": 0; "status": "pending"', 
                               '"job_id": job_id, "progress": 0, "status": "pending"')
    content = content.replace('"job_id": job_id, "progress": 0; "status": "pending"', 
                               '"job_id": job_id, "progress": 0, "status": "pending"')
    
    # 6. Corrigir returns com "ok": True;
    content = re.sub(r'("ok":\s*True)\s*;\s*(")', r'\1, \2', content)
    content = re.sub(r'("ok":\s*False)\s*;\s*(")', r'\1, \2', content)
    
    if content != original:
        with open(api_path + '.bak', 'w', encoding='utf-8') as f:
            f.write(original)
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Corrigido! Backup salvo em {api_path}.bak")
        return True
    else:
        print("Nenhuma alteração necessária")
        return False

if __name__ == "__main__":
    fix_api_syntax()
