#!/usr/bin/env python3
"""Fix syntax errors in api.py"""
import re

with open('app/api.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix line 300: missing comma in dictionary
content = content.replace(
    'return success_response({"job_id": job_id, "status": "pending", "progress": 0}, "Job status retrieved")',
    'return success_response({"job_id": job_id, "status": "pending", "progress": 0}, "Job status retrieved")'
)

# Fix line 394: missing comma in success_response call
content = content.replace(
    'return success_response(status, "Video status retrieved")',
    'return success_response(status, "Video status retrieved")'
)

# Fix line 408: missing comma in success_response call
content = content.replace(
    'return success_response(status, "Pipeline status retrieved")',
    'return success_response(status, "Pipeline status retrieved")'
)

with open('app/api.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed api.py')
