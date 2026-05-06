cd "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"

$python = "K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe"

& $python -c "
import re, os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: encoding='utf-8' -> encoding='utf-8' (hyphen fix)
    content = content.replace(\"encoding='utf-8\\\"\", \"encoding='utf-8\\\"\")
    
    # Fix 2: Extra parenthesis in read_text calls
    # read_text(encoding='utf-8\\\"\")) -> read_text(encoding='utf-8\\\"\")
    content = re.sub(r'read_text\(encoding=\\\\"utf-8\\\"\\)\)', 'read_text(encoding=\\\\"utf-8\\\"\")', content)
    
    # Fix 3: Missing commas in dicts
    # {ok: True \"version\": -> {ok: True, \"version\":
    content = re.sub(r'\\{\\'ok\\': (True|False)\\s+\\\"', r'{\'ok\\': \\1, \\"', content)
    
    # Fix 4: max(result[score] - 20, 0) -> max(result[score] - 20, 0)
    content = content.replace('max(result[\\\"score\\"] - 20, 0)', 'max(result[\\\"score\\"], 20, 0)')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Fixed: ' + filepath)
    else:
        print('No changes: ' + filepath)

fix_file('app/services/script_service.py')
fix_file('app/main.py')
fix_file('app/api.py')
if os.path.exists('pipelines/auto_pipeline.py'):
    fix_file('pipelines/auto_pipeline.py')

print('Done')
"
