#!/usr/bin/env python3
"""Check syntax of all .py files recursively."""
import os
import py_compile
import sys

errors = []
ok = []

for root, dirs, files in os.walk('.'):
    # Skip .git and __pycache__
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
    
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            try:
                py_compile.compile(filepath, doraise=True)
                ok.append(filepath)
            except Exception as e:
                errors.append((filepath, str(e)))

print(f'Total files: {len(ok) + len(errors)}')
print(f'OK: {len(ok)}')
print(f'Errors: {len(errors)}')
print()

if errors:
    print('=== FILES WITH SYNTAX ERRORS ===')
    for fp, err in errors:
        print(f'{fp}')
        print(f'  {err}')
        print()
else:
    print('ALL FILES OK - NO SYNTAX ERRORS FOUND')
