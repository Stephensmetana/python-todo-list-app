# Python ToDo List App

This is a simple command-line ToDo List application written in Python, using SQLite for storage.

## Features
- Add a todo (with priority, creation and last updated timestamps)
- List all todos
- List todos by status (TODO, IN_PROGRESS, DONE)
- List todos by priority (LOW, MEDIUM, HIGH)
- List all todos sorted by priority (HIGH > MEDIUM > LOW)
- Search todos by title substring
- Search todos by tag
- Update a todo (title, description, tags, status, priority)
- Delete a todo
- Export/import todos to/from CSV or JSON
- Tag management: list, rename, delete tags
- Bulk actions: update status, delete, update priority for multiple todos

## Setup
1. Clone the repository or copy the code to your machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python -m todo_app.main init-db
   ```

## Usage
Run the CLI with:
```bash
python -m todo_app.main <command> [options]
```



### Commands

  - `add <title> [--description DESC] [--tags TAG [TAG ...]] [--priority 1-5]`  
    Add a new todo. (1 = highest priority, 5 = lowest)

- `list`  
  List all todos.

- `status <TODO|IN_PROGRESS|DONE>`  
  List todos by status.

  - `priority <1-5>`  
    List todos by priority (1 = highest, 5 = lowest).

- `list-sorted-priority`  
  List all todos sorted by priority (HIGH > MEDIUM > LOW).

- `search-title <substring>`  
  Search todos by title substring.

- `search-tag <tag>`  
  Search todos by tag.

  - `update <id> [--title TITLE] [--description DESC] [--tags TAG [TAG ...]] [--status STATUS] [--priority 1-5]`  
    Update a todo by ID.

- `delete <id>`  
  Delete a todo by ID.

- `export <json|csv> <filepath>`  
  Export all todos to a file (JSON or CSV).

- `import <json|csv> <filepath>`  
  Import todos from a file (JSON or CSV).

- `list-tags`  
  List all tags used in todos.

- `rename-tag <old_tag> <new_tag>`  
  Rename a tag in all todos.

- `delete-tag <tag>`  
  Delete a tag from all todos.

- `bulk-update-status <TODO|IN_PROGRESS|DONE> <id> [<id> ...]`  
  Update status for multiple todos by ID.

- `bulk-delete <id> [<id> ...]`  
  Delete multiple todos by ID.

  - `bulk-update-priority <1-5> <id> [<id> ...]`  
    Update priority for multiple todos by ID.

- `init-db`  
  Initialize the database (run this once before using the app).


## Example
```bash
# Add a todo with priority
python -m todo_app.main add "Buy milk" --description "From the store" --tags shopping urgent --priority 1

# List all todos
python -m todo_app.main list

# List todos by status
python -m todo_app.main status TODO
# Example output:
ID: 1a2b3c
Title: Buy groceries
Description: Buy milk and eggs
Tags: ['shopping', 'urgent']
Status: TODO
Priority: 2
Created: 2025-11-22 10:00:00
Updated: 2025-11-22 10:00:00

ID: 2b3c4d
Title: Read book
Description: Finish reading "Python 101"
Tags: ['reading']
Status: TODO
Priority: 3
Created: 2025-11-21 09:00:00
Updated: 2025-11-21 09:30:00

# List todos by priority
python -m todo_app.main priority 1
# Example output:
ID: 3c4d5e
Title: Write report
Description: Monthly sales report
Tags: ['work']
Status: DONE
Priority: 1
Created: 2025-11-20 08:00:00
Updated: 2025-11-20 12:00:00

# List all todos sorted by priority
python -m todo_app.main list-sorted-priority
# Example output:
ID: 3c4d5e
Title: Write report
Description: Monthly sales report
Tags: ['work']
Status: DONE
Priority: 1
Created: 2025-11-20 08:00:00
Updated: 2025-11-20 12:00:00

ID: 1a2b3c
Title: Buy groceries
Description: Buy milk and eggs
Tags: ['shopping', 'urgent']
Status: TODO
Priority: 2
Created: 2025-11-22 10:00:00
Updated: 2025-11-22 10:00:00

ID: 2b3c4d
Title: Read book
Description: Finish reading "Python 101"
Tags: ['reading']
Status: IN_PROGRESS
Priority: 3
Created: 2025-11-21 09:00:00
Updated: 2025-11-21 09:30:00

# Search by title or tag
python -m todo_app.main search-title milk
# Example output:
ID: 1a2b3c
Title: Buy groceries
Description: Buy milk and eggs
Tags: ['shopping', 'urgent']
Status: TODO
Priority: 2
Created: 2025-11-22 10:00:00
Updated: 2025-11-22 10:00:00

python -m todo_app.main search-tag shopping

# Update a todo
python -m todo_app.main update <id> --status DONE --priority 5

# Delete a todo
python -m todo_app.main delete <id>

# Export/import todos
python -m todo_app.main export json todos.json
python -m todo_app.main import json todos.json

# Tag management
python -m todo_app.main list-tags
python -m todo_app.main rename-tag urgent important
python -m todo_app.main delete-tag shopping

# Bulk actions
python -m todo_app.main bulk-update-status DONE <id1> <id2>
python -m todo_app.main bulk-delete <id1> <id2>
python -m todo_app.main bulk-update-priority 1 <id1> <id2>
```

## Testing
Run the test suite with:
```bash
pytest
```

## File Structure
- `todo_app/models.py` - Data models and enums
- `todo_app/storage.py` - Database logic
- `todo_app/main.py` - CLI interface
- `tests/test_storage.py` - Test suite



## Loading and Saving ToDo Lists (Import/Export)

If you are using a client to wrap this app, you will likely want to load a todo list from a file at the start of each session and save it at the end. This app supports importing and exporting todo lists in both CSV and JSON formats.

### Loading a New ToDo List from CSV (Recommended at Session Start)

To start with a fresh todo list, use the `import-new` command. This will delete any existing database and load todos from your CSV file:

```bash
python -m todo_app.main import-new csv example_import.csv
```

You can use your own CSV file, or use the provided `example_import.csv` as a template. The CSV file must have the following columns:

```
id,title,description,tags,status,priority,created_at,updated_at
```

Example row:

```
1a2b3c,Buy groceries,Buy milk and eggs,"["shopping","urgent"]",TODO,2,2025-11-22T10:00:00,2025-11-22T10:00:00
```

### Saving the ToDo List to CSV (Recommended at Session End)

To save the current state of your todo list to a CSV file, use the `export` command:

```bash
python -m todo_app.main export csv my_todos.csv
```

This will write all current todos to `my_todos.csv`, which you can then load in a future session using `import-new`.

### Typical Client Workflow

1. **At the start of a session:**
    - Load the todo list from a CSV file:
      ```bash
      python -m todo_app.main import-new csv my_todos.csv
      ```
2. **During the session:**
    - Use the CLI or your client to add, update, or delete todos as needed.
3. **At the end of a session:**
    - Save the current todo list to a CSV file:
      ```bash
      python -m todo_app.main export csv my_todos.csv
      ```

This ensures your todo list is always up to date and portable between sessions and clients.

---
## Example Scenario: Building a Shopping List App

Here’s a practical example of how you might use this app to manage your tasks while building a shopping list application.

### 1. Start a New Project Session
Start with a fresh todo list (optional, but recommended):
```bash
python -m todo_app.main import-new csv example_import.csv  # or your own CSV file
```

### 2. Add Todos for Each Step
Add todos for each major step in your project:
```bash
python -m todo_app.main add "Define requirements and features" --priority 1
python -m todo_app.main add "Implement feature: add items to list" --priority 2
python -m todo_app.main add "Implement feature: remove items from list" --priority 2
python -m todo_app.main add "Testing" --priority 3
python -m todo_app.main add "Documentation" --priority 4
```

### 3. List and Review Todos
See all your tasks:
```bash
python -m todo_app.main list
```
Or filter by priority:
```bash
python -m todo_app.main priority 1
```

### 4. Update and Complete Tasks
Mark a task as complete:
```bash
python -m todo_app.main update <id> --status DONE
```
Update a task’s title or priority:
```bash
python -m todo_app.main update <id> --title "Implement feature: edit items in list" --priority 2
```

### 5. Use Tags for Organization (Optional)
Add tags when creating or updating todos:
```bash
python -m todo_app.main add "Deploy to production" --tags deploy release --priority 5
```
List all tags:
```bash
python -m todo_app.main list-tags
```

### 6. Save Your Progress at the End of the Session
Export your current todo list to a CSV file:
```bash
python -m todo_app.main export csv my_shoppinglist_todos.csv
```

You can load this file in your next session using `import-new`.

---