import json
from datetime import datetime
from pathlib import Path
from app.config import PROJECTS_DIR

def create_project(name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pid = "{}_{}".format(ts, name)
    root = PROJECTS_DIR / pid
    dirs = ["brief", "script", "prompts", "storyboard", "renders", "audio", "final", "logs"]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
    project = {
        "id": pid,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "scenes": [],
        "status": "draft"
    }
    (root / "project.json").write_text(json.dumps(project, indent=2, ensure_ascii=False), encoding="utf-8")
    return project

def load_project(pid):
    path = PROJECTS_DIR / pid / "project.json"
    return json.loads(path.read_text(encoding="utf-8"
