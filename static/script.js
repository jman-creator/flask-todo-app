const API_URI = "/api/todos";
const todoList = document.querySelector("#todoList");
const taskInput = document.querySelector("#taskInput");

taskInput.addEventListener("keydown", event => {
    if (event.key === "Enter") addTodo();
});

// Fetch and display todos
async function loadTodos() {
    const res = await fetch(API_URI);
    const todos = await res.json();

    todoList.innerHTML = "";
    todos.forEach(todo => {
        const li = document.createElement("li");
        li.innerHTML = `
            <div class="d-flex gap-2 text-break">
                <input class="form-check-input" type="checkbox" ${todo.done ? "checked" : ""}
                onchange="toggleDone(${todo.id}, this.checked)">
                ${todo.task}
            </div>
            <div class="d-flex gap-2">
                <button class="btn btn-outline-primary" onclick="editTask(${todo.id}, '${todo.task}')">✏️</button>
                <button class="btn btn-outline-danger" onclick="deleteTodo(${todo.id})">❌</button>
            </div>
        `;
        li.className = "list-group-item d-flex align-items-center justify-content-between";
        todoList.appendChild(li);
    });
}

// Add a new todo
async function addTodo() {
    const task = taskInput.value.trim();
    if (!task) return;

    await fetch(API_URI, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ task })
    });

    taskInput.value = "";
    loadTodos();
}

// Toggle todo status
async function toggleDone(id, done) {
    await fetch(`${API_URI}/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ done })
    });
    loadTodos();
}

// Edit todo task
async function editTask(id, taskText) {
    const task = prompt("Edit task:", `${taskText.trim()}`);
    if (!task) return;

    await fetch(`${API_URI}/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ task })
    });
    loadTodos();
}

// Delete a todo
async function deleteTodo(id) {
    await fetch(`${API_URI}/${id}`, {method: "DELETE"});
    loadTodos();
}

// Load todos on page load
window.onload = loadTodos;