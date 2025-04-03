
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Example TodoLists with fix uuid
todo_lists = [
    {'id': '1318d3d1-d979-47e1-a225-dab1751dbe75', 'name': 'Einkaufsliste'},
    {'id': '3062dc25-6b80-4315-bb1d-a7c86b014c65', 'name': 'Arbeit'},
    {'id': '44b02e00-03bc-451d-8d01-0c67ea866fee', 'name': 'Privat'},
    {'id': '123dbe00-02df-4643-adcb-0c1234378900', 'name': 'Programmieren'},
]

# Example tasks for todo_lists
todos = [
    {'id': str(uuid.uuid4()), 'name': 'Milch', 'description': '', 'list': '1318d3d1-d979-47e1-a225-dab1751dbe75'},
    {'id': str(uuid.uuid4()), 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': '3062dc25-6b80-4315-bb1d-a7c86b014c65'},
    {'id': str(uuid.uuid4()), 'name': 'Kinokarten kaufen', 'description': '', 'list': '44b02e00-03bc-451d-8d01-0c67ea866fee'},
    {'id': str(uuid.uuid4()), 'name': 'Eier', 'description': '', 'list': '1318d3d1-d979-47e1-a225-dab1751dbe75'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 1.0', 'description': '/todo-lists GET', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 2.0', 'description': '/todo-list/<list_id>/entries GET', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 3.0', 'description': '/todo-list/<list_id> GET', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 3.1', 'description': '/todo-list/<list_id> DELETE', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 4.0', 'description': '/todo-list POST', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 5.0', 'description': '/todo-list/<list_id>/entry POST', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 6.0', 'description': '/todo-list/<list_id>/entry/<entry_id> PUT', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
    {'id': str(uuid.uuid4()), 'name': 'ToDoList API 6.1', 'description': '/todo-list/<list_id>/entry/<entry_id> DELETE', 'list': '123dbe00-02df-4643-adcb-0c1234378900'},
]

@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

#Search for a specific list via uuid
def search_list(list_id):
    for todo_list in todo_lists:
        if todo_list['id'] == list_id:
            print(f"debug: {todo_list}")
            return todo_list
    return None

#Search for a specific task in a specific list via uuids
def search_task(entry_id, list_id):
    for todo in todos:
        if todo['id'] == entry_id and todo['list'] == list_id:
            print(f"debug: {todo}")
            return todo
    return None

#GET: response = list of all tasks of specific todo_list
# entry: id, name, description                                  -> hier wird noch die list-id it angeben yaml passt nicht //TODO
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_entries_of_list(list_id):
    entries = []
    for todo in todos:
        if todo['list'] == list_id:
            entry = {
                'id':todo['id'],
                'name':todo['name'],
                'description':todo['description']
            }
            entries.append(entry)
    if not entries:
        abort(404, description="List ID not found or no entries")
    print(f"debug: {entries}")
    return jsonify(entries), 200

#GET: response = list of attributes of specific list
# response: id, name
#DELETE:delete todo_list with inherit tasks
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    the_list = search_list(list_id)
    if not the_list:
        abort(404, description="List not found")
    if request.method == 'GET':
        return jsonify(the_list), 200
    if request.method == 'DELETE':
        todo_lists.remove(the_list)
        for todo in todos:
            if todo['list'] == list_id:
                print(f'debug todo: {todo}')
                todos.remove(todo)
        return jsonify({"msg": "success"}), 200

#PUT: update a specific task of a specific todo_list
#response: id,name,description
#DELETE: delete specific task of specific todo_list <<PASST>>
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_list_item(list_id, entry_id):
    the_entry = search_task(entry_id, list_id)
    if not the_entry:
        abort(404, description="Entry not found")
    if request.method == 'PUT':
        updated_data = request.get_json(force=True)
        updated_data['id'] = entry_id
        the_entry.update(updated_data)
        entry = []
        entry = {
            'id':the_entry['id'],
            'name':the_entry['name'],
            'description':the_entry['description']
        }
        return jsonify(entry), 200
    if request.method == 'DELETE':
        todos.remove(the_entry)
        return jsonify({"msg": "success"}), 200

#POST: adds task in specific todo_list
# entry: id, name, description
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    if not search_list(list_id):
        abort(404, description="List ID not found")
    new_entry = request.get_json(force=True)
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id    
    todos.append(new_entry)
    entry = []
    entry = {
        'id':new_entry['id'],
        'name':new_entry['name'],
        'description':new_entry['description']
    }
    return jsonify(entry), 201

#POST: adds todo_list to todo_lists
# response: id,name
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 201

#GET: response = list of all todo_lists
#response: id,name
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
