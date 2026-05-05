#!/usr/bin/env python3
"""Fix the entire script_service.py by rewriting the problematic function."""
import os

filepath = 'app/services/script_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We'll replace from line 291 (0-index 290) to the line before the next function that starts at line 314 (0-index 313?) 
# Actually, let's just replace the whole function from line 291 to line 313 (inclusive) and then keep the rest.
# But we saw duplicate content after line 313. Let's just replace from line 290 to line 350 with a clean version and then append the rest after line 350? 
# Better: Let's find the end of the function by looking for the next line that starts with 'def ' after line 291, and has the same indentation (0 spaces) as the function definition.

start_idx = None
for i, line in enumerate(lines):
    if line.startswith('def restore_previous_version'):
        start_idx = i
        break

if start_idx is None:
    print("Could not find function")
    exit(1)

# Find end of function: next line that starts with 'def ' (not indented) or end of file
end_idx = None
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('def ') and lines[i][4] != ' ':  # function definition starts at column 0
        end_idx = i
        break
if end_idx is None:
    end_idx = len(lines)

# Build the correct function
correct_func = [
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

# Replace
new_lines = lines[:start_idx] + correct_func + lines[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Replaced lines {start_idx+1} to {end_idx} with correct function")