from fastapi import FastAPI
from pydantic import BaseModel
# Pickle
import pickledb
app = FastAPI()

db = pickledb.load('kanban.db', True) 
print(list(db.getall()))
if ("To Do" not in list(db.getall())):
    print("Creating To Do")
    db.lcreate('To Do')
if ("In Progress" not in list(db.getall())):
    print("Creating In Progress")
    db.lcreate('In Progress')
if ("Done" not in list(db.getall())):
    print("Creating Done")
    db.lcreate('Done')
tablemap = {
    0: 'To Do',
    1: 'In Progress',
    2: 'Done'
}

# Structs

class TaskCreateInput(BaseModel):
    table_id: int
    task_name: str

class TaskMoveInput(BaseModel):
    table_to: int
    task_name: str

class TaskEditInput(BaseModel):
    task_name_old: str
    task_name_new: str
    
class TaskDeleteInput(BaseModel):
    task_name: str

@app.get("/")
def read_root():
    return { "Hello": "World" }

# Get all (Tables: tasks)
@app.get("/all")
def get_all():
    # Get all tables
    return [db.lgetall('To Do'), db.lgetall('In Progress'), db.lgetall('Done')]

# Tasks
## Create
@app.post('/task/create')
def create_task(input: TaskCreateInput):
    # Ensure table in bounds
    if not input.table_id in tablemap.keys():
        return { "error": "Table not found" }
    # Ensure task does not exist in all tables
    if input.task_name in db.lgetall('To Do') or input.task_name in db.lgetall('In Progress') or input.task_name in db.lgetall('Done'):
        return { "error": "Task already exists" }

    # Add task to table
    db.ladd(tablemap[input.table_id], input.task_name)
    return { "success": "Task created" }
    
## Edit
@app.post('/task/edit')
def edit_task(input: TaskEditInput):
    # find task in all tables
    for table in tablemap.values():
        if input.task_name_old in db.lgetall(table):
            db.lremvalue(table, input.task_name_old)
            db.ladd(table, input.task_name_new)
            db.dump()
            return { "success": "Task edited" }

## Delete
@app.delete('/task/delete')
def delete_task(input: TaskDeleteInput):
    # find task in all tables
    for table in tablemap.values():
        if input.task_name in db.lgetall(table):
            db.lremvalue(table, input.task_name)
            db.dump()
            return { "success": "Task deleted" }

    # Task not found
    return { "error": "Task not found" }

## Move
@app.put('/task/move')
def move_task(input: TaskMoveInput):
    # Ensure both tables in bounds
    if not input.table_to in tablemap.keys():
        return { "error": "Table to not found" }

    # Remove task from old table
    if delete_task(TaskDeleteInput(task_name=input.task_name)) == { "error": "Task not found" }:
        return { "error": "Task not found" }

    # Add task to new table
    if create_task(TaskCreateInput(table_id=input.table_to, task_name=input.task_name)) == { "error": "Task already exists" }:
        return { "error": "Task already exists" }

    db.dump()
    return { "success": "Task moved" }
