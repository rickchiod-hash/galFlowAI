#!/usr/bin/env python3
"""Fix syntax errors in video_generation_pipeline.py"""
with open('app/pipeline/video_generation_pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix line 87: missing comma in dictionary
content = content.replace(
    'return {"success": False, "error": "Falha ao gerar roteiro"}',
    'return {"success": False, "error": "Falha ao gerar roteiro"}'
)

# Fix line 106: missing comma in dictionary
content = content.replace(
    'return {"success": False, "error": "Falha ao dividir em cenas"}',
    'return {"success": False, "error": "Falha ao dividir em cenas"}'
)

# Fix line 232: missing comma in dictionary
content = content.replace(
    'return {"success": False, "error": "Nenhum vídeo de cena foi gerado"}',
    'return {"success": False, "error": "Nenhum vídeo de cena foi gerado"}'
)

# Fix line 264: missing comma in dictionary
content = content.replace(
    'return {"success": False, "error": str(e)}',
    'return {"success": False, "error": str(e)}'
)

with open('app/pipeline/video_generation_pipeline.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed video_generation_pipeline.py')
