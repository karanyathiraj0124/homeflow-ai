from pathlib import Path
import json
from datetime import datetime, timezone
from threading import Lock

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "tasks.json"
LOCK = Lock()

mcp = FastMCP("HomeFlow AI", json_response=True, stateless_http=True)

def _load():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def _save(tasks):
    DATA_DIR.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

@mcp.tool()
def list_tasks() -> dict:
    """List all HomeFlow tasks, including completion status."""
    with LOCK:
        return {"tasks": _load()}

@mcp.tool()
def add_task(title: str, due_date: str = "", priority: str = "medium") -> dict:
    """Create a task. priority must be low, medium, or high. due_date is optional free text."""
    title = title.strip()
    if not title:
        return {"ok": False, "error": "Task title cannot be empty."}
    if priority not in {"low", "medium", "high"}:
        return {"ok": False, "error": "Priority must be low, medium, or high."}
    with LOCK:
        tasks = _load()
        task = {
            "id": max([t["id"] for t in tasks], default=0) + 1,
            "title": title[:180],
            "due_date": due_date.strip()[:80],
            "priority": priority,
            "completed": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        tasks.append(task)
        _save(tasks)
    return {"ok": True, "task": task}

@mcp.tool()
def complete_task(task_id: int) -> dict:
    """Mark a task as complete by its numeric task_id."""
    with LOCK:
        tasks = _load()
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                _save(tasks)
                return {"ok": True, "task": task}
    return {"ok": False, "error": f"Task {task_id} was not found."}

@mcp.tool()
def delete_task(task_id: int) -> dict:
    """Delete a task by its numeric task_id."""
    with LOCK:
        tasks = _load()
        updated = [t for t in tasks if t["id"] != task_id]
        if len(updated) == len(tasks):
            return {"ok": False, "error": f"Task {task_id} was not found."}
        _save(updated)
    return {"ok": True, "deleted_id": task_id}

if __name__ == "__main__":
    # Streamable HTTP endpoint at http://127.0.0.1:8000/mcp
    mcp.run(transport="streamable-http")
