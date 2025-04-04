# Project
This is a REST API Project for managing Todo lists and inherit Tasks. Using uuid for unique identifier for both.

# Librarys
- uuid 

# Web-Framework-Librarys
- flask 

# Functions
- Create, read, update, delete (CRUD) for list
- CRUD for tasks in list
- uuid for unique identifier for lists and tasks
  
# Setup
### 1. Open Directory in CMD where the Project should be saved.

### 2. Clone Repository:
```bash
https://github.com/AlbelNox/ToDoList.git
```

### 3. Redirect in projectfolder:
```bash
cd <your path>\ToDoList\src
```

### 4. Install requirements:
```bash
pip install -r requirements.txt
```

### 5. Run application:
```bash
python server.py
```

### 6. Server startet:
> http://127.0.0.1:5000 (default)

# Endpoints
## Get all lists

```html
/todo-lists
```

## Create new list
```html
/todo-list
```

Requiement Example:
```json
{ "name": "Example Name" }
```

## Get information of speficic list
```html
/todo-list/<list_id>
```

## Delete list with entries
```html
/todo-list/<list_id>	 
```

## Create new entry
```html
/todo-list/<list_id>/entry
```
Requiement Example:
```json
{
"name": "Example Name",
"description": "Example description"
}
```
                           
## Update entry
```html
/todo-list/<list_id>/entry/<entry_id>
```
Requiement Example:
```json
{
"name": "Example Name",
"description": "Example description"
}
```                        

## Delete entry

```html
/todo-list/<list_id>/entry/<entry_id>
```   
  	    
# LICENCE
Dieses Projekt steht under der MIT-Lizenz. Siehe die [LICENCE](https://github.com/AlbelNox/ToDoList/blob/main/LICENSE) Datei für mehr Informationen.
