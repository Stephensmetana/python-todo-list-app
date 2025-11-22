from typing import List, Optional, Dict
from todo_app.models import TodoItem, TodoCreate, TodoUpdate, TodoStatus
# Get todos by priority

def get_by_id(tid: str) -> Optional[TodoItem]:
    conn = _conn()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    conn.close()
    if row:
        return _row_to_item(row)
    return None

def get_by_priority(priority: int) -> List[TodoItem]:
    conn = _conn()
    rows = conn.execute("SELECT * FROM todos WHERE priority = ? ORDER BY created_at DESC", (priority,)).fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

# Get all todos sorted by priority (HIGH > MEDIUM > LOW)
def get_all_sorted_by_priority() -> List[TodoItem]:
    conn = _conn()
    rows = conn.execute(
        "SELECT * FROM todos ORDER BY priority ASC, created_at DESC"
    ).fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]
# Bulk update status for multiple todos
def bulk_update_status(ids: List[str], status: str) -> int:
    conn = _conn()
    updated_at = datetime.utcnow().isoformat()
    qmarks = ','.join('?' for _ in ids)
    sql = f"UPDATE todos SET status=?, updated_at=? WHERE id IN ({qmarks})"
    cur = conn.execute(sql, (status, updated_at, *ids))
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count

# Bulk delete todos by IDs
def bulk_delete(ids: List[str]) -> int:
    conn = _conn()
    qmarks = ','.join('?' for _ in ids)
    sql = f"DELETE FROM todos WHERE id IN ({qmarks})"
    cur = conn.execute(sql, (*ids,))
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count

# Bulk update priority for multiple todos
def bulk_update_priority(ids: List[str], priority: int) -> int:
    conn = _conn()
    updated_at = datetime.utcnow().isoformat()
    qmarks = ','.join('?' for _ in ids)
    sql = f"UPDATE todos SET priority=?, updated_at=? WHERE id IN ({qmarks})"
    cur = conn.execute(sql, (priority, updated_at, *ids))
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count
from typing import List, Optional, Dict
from todo_app.models import TodoItem, TodoCreate, TodoUpdate, TodoStatus

def get_by_id(tid: str) -> Optional[TodoItem]:
    conn = _conn()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    conn.close()
    if row:
        return _row_to_item(row)
    return None
# List all unique tags
def list_tags() -> List[str]:
    conn = _conn()
    rows = conn.execute("SELECT tags FROM todos").fetchall()
    conn.close()
    tag_set = set()
    for r in rows:
        tags = json.loads(r["tags"] or "[]")
        tag_set.update(tags)
    return sorted(tag_set)

# Rename a tag in all todos
def rename_tag(old_tag: str, new_tag: str) -> int:
    conn = _conn()
    rows = conn.execute("SELECT id, tags FROM todos").fetchall()
    count = 0
    for r in rows:
        tags = json.loads(r["tags"] or "[]")
        if old_tag in tags:
            tags = [new_tag if t == old_tag else t for t in tags]
            conn.execute("UPDATE todos SET tags=? WHERE id=?", (json.dumps(tags), r["id"]))
            count += 1
    conn.commit()
    conn.close()
    return count

# Delete a tag from all todos
def delete_tag_from_all(tag: str) -> int:
    conn = _conn()
    rows = conn.execute("SELECT id, tags FROM todos").fetchall()
    count = 0
    for r in rows:
        tags = json.loads(r["tags"] or "[]")
        if tag in tags:
            tags = [t for t in tags if t != tag]
            conn.execute("UPDATE todos SET tags=? WHERE id=?", (json.dumps(tags), r["id"]))
            count += 1
    conn.commit()
    conn.close()
    return count
import csv
# Export todos to JSON file
def export_todos_json(filepath: str):
    todos = get_all()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump([todo.__dict__ for todo in todos], f, default=str, indent=2)

# Import todos from JSON file
def import_todos_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        # Avoid duplicate IDs
        if 'id' in item:
            existing = get_by_id(item['id']) if 'get_by_id' in globals() else None
            if existing:
                continue
        todo = TodoCreate(
            title=item['title'],
            description=item.get('description'),
            tags=item.get('tags', []),
            priority=int(item.get('priority', 3))
        )
        insert_todo(todo)

# Export todos to CSV file
def export_todos_csv(filepath: str):
    todos = get_all()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'description', 'tags', 'status', 'priority', 'created_at', 'updated_at'])
        for t in todos:
            writer.writerow([
                t.id, t.title, t.description, json.dumps(t.tags), t.status, t.priority, t.created_at, t.updated_at
            ])

# Import todos from CSV file
def import_todos_csv(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            todo = TodoCreate(
                title=row['title'],
                description=row.get('description'),
                tags=json.loads(row['tags']) if row.get('tags') else [],
                priority=int(row.get('priority', 3))
            )
            insert_todo(todo)

# todo_app/storage.py
import sqlite3
from typing import Optional, List, Dict
import json
from datetime import datetime
from .models import TodoItem, TodoCreate, TodoUpdate, TodoStatus
import uuid

DB_PATH = "todos.db"

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 3,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

def _conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _conn()
    conn.execute(CREATE_SQL)
    conn.commit()
    conn.close()

def _row_to_item(row) -> TodoItem:
    return TodoItem(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        tags=json.loads(row["tags"]) if row["tags"] else [],
        status=row["status"],
        priority=int(row["priority"]) if "priority" in row.keys() else 3,
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"])
    )

def insert_todo(todo_create: TodoCreate) -> TodoItem:
    conn = _conn()
    now = datetime.utcnow().isoformat()
    tid = str(uuid.uuid4())
    tags_json = json.dumps(todo_create.tags or [])
    conn.execute(
        "INSERT INTO todos (id,title,description,tags,status,priority,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (tid, todo_create.title, todo_create.description, tags_json, TodoStatus.TODO, int(todo_create.priority), now, now)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    conn.close()
    return _row_to_item(row)


def get_all() -> List[TodoItem]:
    conn = _conn()
    rows = conn.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

def get_by_id(tid: str) -> Optional[TodoItem]:
    conn = _conn()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    conn.close()
    if row:
        return _row_to_item(row)
    return None

def get_by_status(status: str):
    conn = _conn()
    rows = conn.execute("SELECT * FROM todos WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

def search_by_title(substr: str):
    conn = _conn()
    like = f"%{substr}%"
    rows = conn.execute("SELECT * FROM todos WHERE title LIKE ? ORDER BY created_at DESC", (like,)).fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

def search_by_tag(tag: str):
    conn = _conn()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    result = []
    for r in rows:
        tags = json.loads(r["tags"] or "[]")
        if tag in tags:
            result.append(_row_to_item(r))
    return result

def update_todo(tid: str, data: TodoUpdate) -> Optional[TodoItem]:
    conn = _conn()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    if not row:
        conn.close()
        return None
    current = _row_to_item(row)
    # Merge updates
    title = data.title if data.title is not None else current.title
    description = data.description if data.description is not None else current.description
    tags = data.tags if data.tags is not None else current.tags
    status = data.status if data.status is not None else current.status
    priority = int(data.priority) if data.priority is not None else current.priority
    updated_at = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE todos SET title=?, description=?, tags=?, status=?, priority=?, updated_at=? WHERE id=?",
        (title, description, json.dumps(tags), status, int(priority), updated_at, tid)
    )
    conn.commit()
    row2 = conn.execute("SELECT * FROM todos WHERE id = ?", (tid,)).fetchone()
    conn.close()
    return _row_to_item(row2)

def delete_todo(tid: str) -> bool:
    conn = _conn()
    cur = conn.execute("DELETE FROM todos WHERE id = ?", (tid,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted

