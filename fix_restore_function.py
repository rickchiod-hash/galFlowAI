#!/usr/bin/env python3
"""Fix the restore_previous_version function in script_service.py."""
import os

filepath = 'app/services/script_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start and end of the function
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def restore_previous_version'):
        start = i
        break

if start is None:
    print("Function not found")
    exit(1)

# Find the end of the function (next line that starts with 'def ' or 'class ' or end of file, with same or less indent)
# Simple approach: find the next line that starts with 'def ' after start
end = None
for i in range(start + 1, len(lines)):
    if lines[i].startswith('def ') or lines[i].startswith('class '):
        end = i
        break
if end is None:
    end = len(lines)

# Build the new function lines
new_func = [
    'def restore_previous_version(project_id: str) -> Dict:\n',
    '    """Restore previous version as current."""\n',
    '    try:\n',
    '        versions = _load_versions(project_id)\n',
    '        if len(versions) < 2:\n',
    '            return {"ok": False, "error": "No previous version to restore"}\n',
    '        \n',
    '        # Get previous version\n',
    '        prev = versions[-2]\n',
    '        version = prev["version"]\n',
    '        \n',
    '        # Load that version\'s script\n',
    '        script_dir = _get_script_dir(project_id)\n',
    '        md_file = script_dir / f"script_{version}.md"\n',
    '        if md_file.exists():\n',
    '            script = md_file.read_text(encoding="utf-8")\n',
    '        else:\n',
    '            return {"ok": False, "error": "Previous version file not found"}\n',
    '        \n',
    '        return {"ok": True, "script": script, "version": version}\n',
    '    except Exception as e:\n',
    '        return {"ok": False, "error": str(e)}\n'
]

# Replace the lines
new_lines = lines[:start] + new_func + lines[end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Fixed function at lines {start+1} to {end}")