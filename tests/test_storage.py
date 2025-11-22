import os
import tempfile
import pytest
import sqlite3
from todo_app import storage
from todo_app.models import TodoCreate, TodoUpdate, TodoStatus

TEST_DB = "test_todos.db"

def setup_module(module):
    # Use a separate test database
    storage.DB_PATH = TEST_DB
    storage.init_db()

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_insert_and_get_all():
    storage.init_db()
    storage.insert_todo(TodoCreate("Test1", "Desc1", ["tag1"], priority=1))
    storage.insert_todo(TodoCreate("Test2", "Desc2", ["tag2"], priority=5))
    todos = storage.get_all()
    assert len(todos) >= 2
    titles = [t.title for t in todos]
    assert "Test1" in titles and "Test2" in titles
    # Check priorities
    t1 = next(t for t in todos if t.title == "Test1")
    t2 = next(t for t in todos if t.title == "Test2")
    assert t1.priority == 1
    assert t2.priority == 5

def test_get_by_status():
    storage.init_db()
    storage.insert_todo(TodoCreate("StatusTest", "", []))
    todos = storage.get_by_status(TodoStatus.TODO)
    assert any(t.title == "StatusTest" for t in todos)

def test_search_by_title():
    storage.init_db()
    storage.insert_todo(TodoCreate("UniqueTitle123", "", []))
    results = storage.search_by_title("UniqueTitle123")
    assert any("UniqueTitle123" in t.title for t in results)

def test_search_by_tag():
    storage.init_db()
    storage.insert_todo(TodoCreate("TagTest", "", ["specialtag"]))
    results = storage.search_by_tag("specialtag")
    assert any("TagTest" == t.title for t in results)

def test_update_todo():
    storage.init_db()
    todo = storage.insert_todo(TodoCreate("ToUpdate", "desc", ["t1"], priority=2))
    updated = storage.update_todo(todo.id, TodoUpdate(title="UpdatedTitle", status=TodoStatus.DONE, priority=4))
    assert updated.title == "UpdatedTitle"
    assert updated.status == TodoStatus.DONE
    assert updated.priority == 4
def test_priority_filter_and_sort():
    storage.init_db()
    storage.insert_todo(TodoCreate("P1", priority=1))
    storage.insert_todo(TodoCreate("P3", priority=3))
    storage.insert_todo(TodoCreate("P5", priority=5))
    p1s = storage.get_by_priority(1)
    assert any(t.title == "P1" for t in p1s)
    sorted_todos = storage.get_all_sorted_by_priority()
    priorities = [t.priority for t in sorted_todos]
    assert priorities == sorted(priorities)
def test_export_import_json(tmp_path):
    storage.init_db()
    storage.insert_todo(TodoCreate("ExportMe", priority=2))
    out = tmp_path / "todos.json"
    storage.export_todos_json(str(out))
    # Clear DB and import
    storage.init_db()
    storage.import_todos_json(str(out))
    todos = storage.get_all()
    assert any(t.title == "ExportMe" for t in todos)
def test_export_import_csv(tmp_path):
    storage.init_db()
    storage.insert_todo(TodoCreate("ExportCSV", priority=3))
    out = tmp_path / "todos.csv"
    storage.export_todos_csv(str(out))
    # Clear DB and import
    storage.init_db()
    storage.import_todos_csv(str(out))
    todos = storage.get_all()
    assert any(t.title == "ExportCSV" for t in todos)
def test_tag_management():
    import tempfile
    with tempfile.NamedTemporaryFile() as db:
        storage.DB_PATH = db.name
        storage.init_db()
        storage.insert_todo(TodoCreate("Tag1", tags=["a", "b"]))
        storage.insert_todo(TodoCreate("Tag2", tags=["b", "c"]))
        tags = storage.list_tags()
        assert set(tags) == {"a", "b", "c"}
        count = storage.rename_tag("b", "z")
        assert count == 2
        tags2 = storage.list_tags()
        assert "z" in tags2 and "b" not in tags2
        count2 = storage.delete_tag_from_all("z")
        assert count2 == 2
        tags3 = storage.list_tags()
        assert "z" not in tags3
def test_bulk_actions():
    storage.init_db()
    t1 = storage.insert_todo(TodoCreate("Bulk1", priority=2))
    t2 = storage.insert_todo(TodoCreate("Bulk2", priority=3))
    t3 = storage.insert_todo(TodoCreate("Bulk3", priority=4))
    # Bulk update status
    n = storage.bulk_update_status([t1.id, t2.id], TodoStatus.DONE)
    assert n == 2
    todos = storage.get_all()
    for t in todos:
        if t.id in [t1.id, t2.id]:
            assert t.status == TodoStatus.DONE
    # Bulk update priority
    n2 = storage.bulk_update_priority([t1.id, t3.id], 1)
    assert n2 == 2
    todos = storage.get_all()
    for t in todos:
        if t.id in [t1.id, t3.id]:
            assert t.priority == 1
    # Bulk delete
    n3 = storage.bulk_delete([t1.id, t2.id])
    assert n3 == 2
    todos = storage.get_all()
    ids = [t.id for t in todos]
    assert t1.id not in ids and t2.id not in ids
def test_timestamps():
    storage.init_db()
    todo = storage.insert_todo(TodoCreate("TimeTest"))
    assert todo.created_at is not None
    assert todo.updated_at is not None
    updated = storage.update_todo(todo.id, TodoUpdate(title="TimeTest2"))
    assert updated.updated_at > todo.updated_at

def test_delete_todo():
    storage.init_db()
    todo = storage.insert_todo(TodoCreate("ToDelete", "desc", []))
    deleted = storage.delete_todo(todo.id)
    assert deleted
    # Should not find it anymore
    todos = storage.get_all()
    assert not any(t.id == todo.id for t in todos)