import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

todos = []
counter = 1

HTML = '''
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud To-Do App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }
        h1 {
            color: #fff;
            font-size: 2rem;
            margin-bottom: 8px;
            text-align: center;
        }
        .subtitle {
            color: rgba(255,255,255,0.4);
            text-align: center;
            font-size: 0.85rem;
            margin-bottom: 30px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .input-row {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        input[type=text] {
            flex: 1;
            padding: 14px 18px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(255,255,255,0.08);
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: border 0.3s;
        }
        input[type=text]::placeholder { color: rgba(255,255,255,0.3); }
        input[type=text]:focus { border-color: #e94560; }
        button.add-btn {
            padding: 14px 22px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #e94560, #c62a47);
            color: #fff;
            font-size: 1.4rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(233,69,96,0.4);
        }
        button.add-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.6); }
        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 16px;
            padding: 0 4px;
        }
        .stats span { color: rgba(255,255,255,0.45); font-size: 0.85rem; }
        .stats .count { color: #e94560; font-weight: 600; }
        .todo-list { list-style: none; }
        .todo-item {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 18px;
            border-radius: 12px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.07);
            margin-bottom: 10px;
            transition: background 0.2s;
        }
        .todo-item:hover { background: rgba(255,255,255,0.09); }
        .todo-item.done { opacity: 0.5; }
        .todo-item.done .todo-text { text-decoration: line-through; }
        .checkbox {
            width: 22px; height: 22px;
            border-radius: 6px;
            border: 2px solid rgba(255,255,255,0.2);
            background: transparent;
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
            transition: all 0.2s;
        }
        .checkbox.checked { background: #e94560; border-color: #e94560; }
        .checkbox.checked::after { content: '✓'; color: #fff; font-size: 13px; font-weight: bold; }
        .todo-text { flex: 1; color: #fff; font-size: 0.95rem; }
        .delete-btn {
            background: none;
            border: none;
            color: rgba(255,255,255,0.2);
            font-size: 1.1rem;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            transition: color 0.2s, background 0.2s;
        }
        .delete-btn:hover { color: #e94560; background: rgba(233,69,96,0.1); }
        .empty {
            text-align: center;
            color: rgba(255,255,255,0.2);
            padding: 30px;
            font-size: 0.9rem;
        }
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #e94560, #c62a47);
            color: #fff;
            font-size: 0.65rem;
            padding: 2px 8px;
            border-radius: 20px;
            margin-left: 8px;
            vertical-align: middle;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>✅ To-Do App <span class="badge">Cloud Native</span></h1>
    <p class="subtitle">Kubernetes • Flask • containerd</p>
    <div class="input-row">
        <input type="text" id="taskInput" placeholder="Adaugă o sarcină nouă..." onkeypress="if(event.key==='Enter')addTodo()">
        <button class="add-btn" onclick="addTodo()">+</button>
    </div>
    <div class="stats">
        <span>Total: <span class="count" id="totalCount">0</span></span>
        <span>Completate: <span class="count" id="doneCount">0</span></span>
        <span>Rămase: <span class="count" id="leftCount">0</span></span>
    </div>
    <ul class="todo-list" id="todoList"></ul>
    <div class="empty" id="emptyMsg">Nicio sarcină. Adaugă una mai sus! 🚀</div>
</div>
<script>
    let todos = [];
    async function load() {
        const r = await fetch('/api/todos');
        todos = await r.json();
        render();
    }
    async function addTodo() {
        const inp = document.getElementById('taskInput');
        const text = inp.value.trim();
        if (!text) return;
        await fetch('/api/todos', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text})});
        inp.value = '';
        load();
    }
    async function toggleTodo(id) {
        await fetch('/api/todos/' + id + '/toggle', {method:'PUT'});
        load();
    }
    async function deleteTodo(id) {
        await fetch('/api/todos/' + id, {method:'DELETE'});
        load();
    }
    function render() {
        const list = document.getElementById('todoList');
        const empty = document.getElementById('emptyMsg');
        list.innerHTML = '';
        if (todos.length === 0) { empty.style.display='block'; }
        else {
            empty.style.display='none';
            todos.forEach(t => {
                const li = document.createElement('li');
                li.className = 'todo-item' + (t.done ? ' done' : '');
                li.innerHTML = `
                    <div class="checkbox ${t.done?'checked':''}" onclick="toggleTodo(${t.id})"></div>
                    <span class="todo-text">${escapeHtml(t.text)}</span>
                    <button class="delete-btn" onclick="deleteTodo(${t.id})">✕</button>`;
                list.appendChild(li);
            });
        }
        document.getElementById('totalCount').textContent = todos.length;
        document.getElementById('doneCount').textContent = todos.filter(t=>t.done).length;
        document.getElementById('leftCount').textContent = todos.filter(t=>!t.done).length;
    }
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    load();
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    global counter
    data = request.get_json()
    todo = {'id': counter, 'text': data['text'], 'done': False}
    todos.append(todo)
    counter += 1
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>/toggle', methods=['PUT'])
def toggle_todo(todo_id):
    for t in todos:
        if t['id'] == todo_id:
            t['done'] = not t['done']
            return jsonify(t)
    return jsonify({'error': 'not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'deleted': todo_id})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)