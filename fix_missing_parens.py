#!/usr/bin/env python3
"""Fix missing closing parentheses in read_text calls."""
import os
import re

files_to_fix = [
    'app/api.py', 'app/api_backup.py', 'app/api_backup_full.py', 
    'app/api_commit_backup.py', 'app/project_manager.py', 
    'app/jobs/queue.py', 'app/services/metrics_service.py', 
    'app/services/script_service.py'
]

for fp in files_to_fix:
    filepath = os.path.join('.', fp)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for i, line in enumerate(lines):
        # Check if line has read_text(encoding="utf-8" without closing
        if 'read_text(encoding="utf-8"' in line and not line.rstrip().endswith('))'):
            # This line needs fixing
            # Check if next line is just a continuation
            if i + 1 < len(lines) and not lines[i+1].strip().startswith(')'):
                # The closing ) is missing, add it
                line = line.rstrip() + '))\n'
                modified = True
        new_lines.append(line)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f'Fixed: {fp}')
    else:
        print(f'No change: {fp}')

print('Done')
