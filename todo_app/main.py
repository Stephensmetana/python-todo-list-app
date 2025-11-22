import argparse
from todo_app import storage
from todo_app.models import TodoCreate, TodoUpdate, TodoStatus, PRIORITY_MIN, PRIORITY_MAX
import sys

def print_todo(todo):
    print(f"ID: {todo.id}\nTitle: {todo.title}\nDescription: {todo.description}\nTags: {todo.tags}\nStatus: {todo.status}\nPriority: {getattr(todo, 'priority', 3)}\nCreated: {todo.created_at}\nUpdated: {todo.updated_at}\n")

def main():
    parser = argparse.ArgumentParser(description="ToDo List CLI App")
    subparsers = parser.add_subparsers(dest="command")

    # Add todo
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", type=str, help="Title of the todo")
    add_parser.add_argument("--description", type=str, help="Description", default=None)
    add_parser.add_argument("--tags", nargs="*", help="Tags", default=None)
    add_parser.add_argument("--priority", type=int, choices=range(PRIORITY_MIN, PRIORITY_MAX+1), default=3, help="Priority (1=highest, 5=lowest)")

    # Get all
    subparsers.add_parser("list", help="List all todos")

    # Get by status
    status_parser = subparsers.add_parser("status", help="List todos by status")
    status_parser.add_argument("status", type=str, choices=[s.value for s in TodoStatus], help="Status")

    # Search by title
    title_parser = subparsers.add_parser("search-title", help="Search todos by title substring")
    title_parser.add_argument("substr", type=str, help="Substring to search in title")

    # Search by tag
    tag_parser = subparsers.add_parser("search-tag", help="Search todos by tag")
    tag_parser.add_argument("tag", type=str, help="Tag to search for")

    # Update todo
    update_parser = subparsers.add_parser("update", help="Update a todo")
    update_parser.add_argument("id", type=str, help="ID of the todo to update")
    update_parser.add_argument("--title", type=str, help="New title", default=None)
    update_parser.add_argument("--description", type=str, help="New description", default=None)
    update_parser.add_argument("--tags", nargs="*", help="New tags", default=None)
    update_parser.add_argument("--status", type=str, choices=[s.value for s in TodoStatus], help="New status", default=None)
    update_parser.add_argument("--priority", type=int, choices=range(PRIORITY_MIN, PRIORITY_MAX+1), help="New priority (1-5)", default=None)

    # Export/Import
    export_parser = subparsers.add_parser("export", help="Export todos to file")
    export_parser.add_argument("format", choices=["json", "csv"], help="Export format")
    export_parser.add_argument("filepath", type=str, help="Output file path")

    import_parser = subparsers.add_parser("import", help="Import todos from file")
    import_parser.add_argument("format", choices=["json", "csv"], help="Import format")
    import_parser.add_argument("filepath", type=str, help="Input file path")

    # Import-new (create new DB and import)
    import_new_parser = subparsers.add_parser("import-new", help="Create a new DB and import todos from file")
    import_new_parser.add_argument("format", choices=["json", "csv"], help="Import format")
    import_new_parser.add_argument("filepath", type=str, help="Input file path")

    # Tag management
    subparsers.add_parser("list-tags", help="List all tags")
    rename_tag_parser = subparsers.add_parser("rename-tag", help="Rename a tag")
    rename_tag_parser.add_argument("old_tag", type=str, help="Old tag name")
    rename_tag_parser.add_argument("new_tag", type=str, help="New tag name")
    delete_tag_parser = subparsers.add_parser("delete-tag", help="Delete a tag from all todos")
    delete_tag_parser.add_argument("tag", type=str, help="Tag to delete")

    # Bulk actions
    bulk_status_parser = subparsers.add_parser("bulk-update-status", help="Bulk update status for todos")
    bulk_status_parser.add_argument("status", type=str, choices=[s.value for s in TodoStatus], help="New status")
    bulk_status_parser.add_argument("ids", nargs="+", help="IDs to update")

    bulk_delete_parser = subparsers.add_parser("bulk-delete", help="Bulk delete todos")
    bulk_delete_parser.add_argument("ids", nargs="+", help="IDs to delete")

    bulk_priority_parser = subparsers.add_parser("bulk-update-priority", help="Bulk update priority for todos")
    bulk_priority_parser.add_argument("priority", type=int, choices=range(PRIORITY_MIN, PRIORITY_MAX+1), help="New priority (1-5)")
    bulk_priority_parser.add_argument("ids", nargs="+", help="IDs to update")

    # Priority filtering/sorting
    priority_parser = subparsers.add_parser("priority", help="List todos by priority")
    priority_parser.add_argument("priority", type=int, choices=range(PRIORITY_MIN, PRIORITY_MAX+1), help="Priority (1-5)")

    subparsers.add_parser("list-sorted-priority", help="List all todos sorted by priority (1=highest)")

    # Delete todo
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=str, help="ID of the todo to delete")

    # Init DB
    subparsers.add_parser("init-db", help="Initialize the database")

    args = parser.parse_args()

    import os

    if args.command == "add":
        todo = storage.insert_todo(TodoCreate(args.title, args.description, args.tags, args.priority))
        print("Added todo:")
        print_todo(todo)
    elif args.command == "list":
        todos = storage.get_all()
        for t in todos:
            print_todo(t)
    elif args.command == "status":
        todos = storage.get_by_status(args.status)
        for t in todos:
            print_todo(t)
    elif args.command == "search-title":
        todos = storage.search_by_title(args.substr)
        for t in todos:
            print_todo(t)
    elif args.command == "search-tag":
        todos = storage.search_by_tag(args.tag)
        for t in todos:
            print_todo(t)
    elif args.command == "update":
        update = TodoUpdate(
            title=args.title,
            description=args.description,
            tags=args.tags,
            status=args.status,
            priority=args.priority
        )
        todo = storage.update_todo(args.id, update)
        if todo:
            print("Updated todo:")
            print_todo(todo)
        else:
            print("Todo not found.")
    elif args.command == "export":
        if args.format == "json":
            storage.export_todos_json(args.filepath)
        else:
            storage.export_todos_csv(args.filepath)
        print(f"Exported todos to {args.filepath}.")
    elif args.command == "import":
        if args.format == "json":
            storage.import_todos_json(args.filepath)
        else:
            storage.import_todos_csv(args.filepath)
        print(f"Imported todos from {args.filepath}.")
    elif args.command == "import-new":
        # Remove DB file if it exists
        if os.path.exists(storage.DB_PATH):
            os.remove(storage.DB_PATH)
        storage.init_db()
        if args.format == "json":
            storage.import_todos_json(args.filepath)
        else:
            storage.import_todos_csv(args.filepath)
        print(f"Created new DB and imported todos from {args.filepath}.")
    elif args.command == "list-tags":
        tags = storage.list_tags()
        print("Tags:", tags)
    elif args.command == "rename-tag":
        count = storage.rename_tag(args.old_tag, args.new_tag)
        print(f"Renamed tag in {count} todos.")
    elif args.command == "delete-tag":
        count = storage.delete_tag_from_all(args.tag)
        print(f"Deleted tag from {count} todos.")
    elif args.command == "bulk-update-status":
        count = storage.bulk_update_status(args.ids, args.status)
        print(f"Updated status for {count} todos.")
    elif args.command == "bulk-delete":
        count = storage.bulk_delete(args.ids)
        print(f"Deleted {count} todos.")
    elif args.command == "bulk-update-priority":
        count = storage.bulk_update_priority(args.ids, args.priority)
        print(f"Updated priority for {count} todos.")
    elif args.command == "priority":
        todos = storage.get_by_priority(args.priority)
        for t in todos:
            print_todo(t)
    elif args.command == "list-sorted-priority":
        todos = storage.get_all_sorted_by_priority()
        for t in todos:
            print_todo(t)
    elif args.command == "delete":
        ok = storage.delete_todo(args.id)
        if ok:
            print("Todo deleted.")
        else:
            print("Todo not found.")
    elif args.command == "init-db":
        storage.init_db()
        print("Database initialized.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()