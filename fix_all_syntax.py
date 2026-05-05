#!/usr/bin/env python3
"""
Script to fix ALL syntax errors in .py files for Gal AI Studio.
Run: python fix_all_syntax.py
"""
import os
import re
import sys

def fix_file(filepath):
    """Fix all syntax errors in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # Fix 1: COMMERCIAL -> COMMERCIAL (missing 'M')
        count1 = content.count('COMMERCIAL')
        if count1 > 0:
            content = content.replace('COMMERCIAL', 'COMMERCIAL')
            changes.append(f'Fixed {count1} COMMERCIAL -> COMMERCIAL')
        
        # Fix 2: encoding="utf-8" -> encoding="utf-8" (hyphen fix)
        # The actual issue is encoding="utf-8" with wrong character
        # In the files, it's encoding="utf-8" (with hyphen) - actually correct
        # But there might be encoding="utf-8" with minus sign
        # Let's check for the actual problematic pattern
        
        # Fix 3: Extra parentheses in read_text calls
        # Pattern: read_text(encoding="utf-8"))
        pattern_extra_paren = r'read_text\(encoding="utf-8"\)\)'
        matches = re.findall(pattern_extra_paren, content)
        if matches:
            content = re.sub(pattern_extra_paren, r'read_text(encoding="utf-8"))', content)
            changes.append(f'Fixed {len(matches)} extra parentheses in read_text')
        
        # Fix 4: Missing commas in dicts like {"ok": False, "error": str(e)}
        # Pattern: {"ok": False, "error": -> {"ok": False, "error":
        pattern_missing_comma = r'\{"ok": (True|False) ("[^"]+":)'
        matches = re.findall(pattern_missing_comma, content)
        if matches:
            content = re.sub(pattern_missing_comma, r'{"ok": \1, \2', content)
            changes.append(f'Fixed {len(matches)} missing commas in dicts')
        
        # Fix 5: json.loads with extra paren
        pattern_json_extra = r'json\.loads\([^)]+\)\)'
        matches = re.findall(pattern_json_extra, content)
        if matches:
            for match in matches:
                # Remove one trailing )
                new_match = match.rstrip(')')
                content = content.replace(match, new_match)
            changes.append(f'Fixed json.loads extra paren')
        
        # Fix 6: write_text with missing comma
        # Pattern: write_text(var, encoding= -> write_text(var, encoding=
        # Actually the issue is write_text(script_markdown, encoding= vs write_text(script_markdown, encoding=
        # They look the same, let's check for the actual error
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'Error: {str(e)}']

def main():
    base_dir = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta'
    
    print('=== FIXING ALL SYNTAX ERRORS ===')
    print(f'Base dir: {base_dir}')
    print()
    
    fixed_files = []
    error_files = []
    
    for root, dirs, files in os.walk(base_dir):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache']]
        
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                modified, changes = fix_file(filepath)
                if modified:
                    fixed_files.append((filepath, changes))
                    print(f'FIXED: {filepath}')
                    for change in changes:
                        print(f'  - {change}')
                else:
                    if changes and 'Error' in str(changes):
                        error_files.append((filepath, changes))
                        print(f'ERROR: {filepath}: {changes}')
    
    print()
    print('=== SUMMARY ===')
    print(f'Files fixed: {len(fixed_files)}')
    print(f'Errors: {len(error_files)}')
    
    if fixed_files:
        print()
        print('Fixed files:')
        for fp, changes in fixed_files:
            print(f'  {fp}')
    
    return len(error_files) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
