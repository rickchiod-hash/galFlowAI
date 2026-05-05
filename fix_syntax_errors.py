#!/usr/bin/env python3
import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: encoding="utf-8" -> encoding="utf-8" (hyphen fix)
    content = content.replace('encoding="utf-8"', 'encoding="utf-8"')
    
    # Fix 2: Extra parenthesis in read_text calls
    # read_text(encoding="utf-8")) -> read_text(encoding="utf-8"))
    content = re.sub(r'read_text\(encoding="utf-8"\)\)', 'read_text(encoding="utf-8"))', content)
    content = re.sub(r'read_text\(encoding="utf-8"\)\s*\)', 'read_text(encoding="utf-8"))', content)
    
    # Fix 3: Extra parenthesis in json.loads calls  
    content = re.sub(r'json\.loads\(([^)]+)\)\)', r'json.loads(\1', content)
    
    # Fix 4: Missing commas in dicts - {"ok": True, "version": ...} 
    # Pattern: {"ok": True, "version": -> {"ok": True, "version":
    content = re.sub(r'\{"ok": (True|False)\s+"', r'{"ok": \1, "', content)
    content = re.sub(r'\{"ok": (True|False), "', r'{"ok": \1, "', content)
    
    # Fix 5: Fix write_text calls with comma issues
    # md_file.write_text(script_markdown, encoding= -> md_file.write_text(script_markdown, encoding=
    content = re.sub(r'write_text\((\w+),\s+encoding=', r'write_text(\1, encoding=', content)
    
    # Fix 6: Fix "error": str(e) missing comma
    content = re.sub(r'\{"ok": False, "error":', r'{"ok": False, "error":', content)
    content = re.sub(r'\{"ok": True, "script":', r'{"ok": True, "script":', content)
    content = re.sub(r'\{"ok": True, "version":', r'{"ok": True, "version":', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
    else:
        print(f"No changes: {filepath}")

# Fix script_service.py
fix_file("app/services/script_service.py")

# Fix main.py  
fix_file("app/main.py")

# Fix auto_pipeline.py
if os.path.exists("pipelines/auto_pipeline.py"):
    fix_file("pipelines/auto_pipeline.py")

# Fix api.py
fix_file("app/api.py")

print("Done fixing syntax errors")
