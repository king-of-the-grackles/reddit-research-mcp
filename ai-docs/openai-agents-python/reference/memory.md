# Memory Reference

## Session

Bases: `Protocol`

Protocol for session implementations.

Session stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management.

### Attributes

#### session_id
```python
session_id: str
```
The unique identifier for the session.

### Methods

#### get_items(async)
```python
async def get_items(limit: int | None = None) -> list[TResponseInputItem]
```
Retrieve the conversation history for this session.

**Args:**
- `limit`: Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order.

**Returns:**
- List of input items representing the conversation history

#### add_items(async)
```python
async def add_items(items: list[TResponseInputItem]) -> None
```
Add new items to the conversation history.

**Args:**
- `items`: List of input items to add to the history

#### pop_item(async)
```python
async def pop_item() -> TResponseInputItem | None
```
Remove and return the most recent item from the session.

**Returns:**
- The most recent item if it exists, None if the session is empty

#### clear_session(async)
```python
async def clear_session() -> None
```
Clear all items for this session.

## SQLiteSession

Bases: `SessionABC`

SQLite-based implementation of session storage.

This implementation stores conversation history in a SQLite database. By default, uses an in-memory database that is lost when the process ends. For persistent storage, provide a file path.

### __init__
```python
def __init__(
    session_id: str,
    db_path: str | Path = ":memory:",
    sessions_table: str = "agent_sessions",
    messages_table: str = "agent_messages",
)
```
Initialize the SQLite session.

**Args:**
- `session_id`: Unique identifier for the conversation session
- `db_path`: Path to the SQLite database file. Defaults to ':memory:' (in-memory database)
- `sessions_table`: Name of the table to store session metadata. Defaults to 'agent_sessions'
- `messages_table`: Name of the table to store message data. Defaults to 'agent_messages'

### Methods

#### get_items(async)
```python
async def get_items(limit: int | None = None) -> list[TResponseInputItem]
```
Retrieve the conversation history for this session.

**Args:**
- `limit`: Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order.

**Returns:**
- List of input items representing the conversation history

#### add_items(async)
```python
async def add_items(items: list[TResponseInputItem]) -> None
```
Add new items to the conversation history.

**Args:**
- `items`: List of input items to add to the history

#### pop_item(async)
```python
async def pop_item() -> TResponseInputItem | None
```
Remove and return the most recent item from the session.

**Returns:**
- The most recent item if it exists, None if the session is empty

#### clear_session(async)
```python
async def clear_session() -> None
```
Clear all items for this session.

#### close()
```python
def close() -> None
```
Close the database connection.

## Implementation Details

The SQLiteSession implementation includes the following features:

- **Thread Safety**: Uses threading locks and thread-local connections for safe concurrent access
- **In-Memory vs File Storage**: Automatically handles both in-memory and file-based databases
- **WAL Mode**: Uses Write-Ahead Logging for better concurrency
- **Automatic Schema Creation**: Creates necessary tables and indexes on initialization
- **JSON Serialization**: Stores message data as JSON for flexibility
- **Timestamp Tracking**: Maintains created_at and updated_at timestamps for sessions
- **Foreign Key Constraints**: Ensures referential integrity between sessions and messages
- **Indexed Queries**: Creates indexes for efficient retrieval by session_id

### Database Schema

The implementation creates two tables:

1. **Sessions Table** (default: `agent_sessions`):
   - `session_id` (TEXT PRIMARY KEY)
   - `created_at` (TIMESTAMP)
   - `updated_at` (TIMESTAMP)

2. **Messages Table** (default: `agent_messages`):
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `session_id` (TEXT NOT NULL)
   - `message_data` (TEXT NOT NULL) - JSON serialized
   - `created_at` (TIMESTAMP)
   - Foreign key reference to sessions table with CASCADE delete