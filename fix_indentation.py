#!/usr/bin/env python3
"""Fix indentation in script_service.py for the restore_previous_version function."""
import os

filepath = 'app/services/script_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We'll replace lines 291-319 (0-indexed 290-318) with corrected version
# But let's just fix the specific function by rewriting from line 291 to the end of the function.

# Instead, let's find the function and replace its body.

new_lines = []
i = 0
while i < len(lines):
    if lines[i].strip().startswith('def restore_previous_version'):
        new_lines.append(lines[i])
        i += 1
        # Add the docstring
        new_lines.append(lines[i])
        i += 1
        # Now we need to add the fixed function body
        new_lines.append('     try:\n')
        new_lines.append('         versions = _load_versions(project_id)\n')
        new_lines.append('         if len(versions) < 2:\n')
        new_lines.append('             return {"ok": False, "error": "No previous version to restore"}\n')
        new_lines.append('         \n')
        new_lines.append('         # Get previous version\n')
        new_lines.append('         prev = versions[-2]\n')
        new_lines.append('         version = prev["version"]\n')
        new_lines.append('         \n')
        new_lines.append('         # Load that version\'s script\n')
        new_lines.append('         script_dir = _get_script_dir(project_id)\n')
        new_lines.append('         md_file = script_dir / f"script_{version}.md"\n')
        new_lines.append('         if md_file.exists():\n')
        new_lines.append('             script = md_file.read_text(encoding="utf-8")\n')
        new_lines.append('         else:\n')
        new_lines.append('             return {"ok": False, "error": "Previous version file not found"}\n')
        new_lines.append('         \n')
        new_lines.append('         return {"ok": True, "script": script, "version": version}\n')
        new_lines.append('     except Exception as e:\n')
        new_lines.append('         return {"ok": False, "error": str(e)}\n')
        # Skip until we see the end of the function (next function or class or end of file)
        # We'll skip lines until we find a line that starts with 'def ' or 'class ' or end of file, but not indented
        i += 1
        while i < len(lines) and not (lines[i].startswith('def ') or lines[i].startswith('class ')) and lines[i].strip() != '':
            i += 1
        # Now we are at the next function/class or empty line, we'll continue the loop without adding the skipped lines
        continue
    else:
        new_lines.append(lines[i])
        i += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Fixed indentation in restore_previous_version function")