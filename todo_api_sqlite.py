from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task, "done": self.done}
    
# Create tables
with app.app_context():
    db.create_all()


# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# GET all todos
@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos])

# GET todo by ID
@app.route("/api/todos/<int:id>", methods=["GET"])
def get_todo(id):
    todo = db.session.get(Todo, id) # Todo.query.get(id) is legacy approach
    if todo:
        return jsonify(todo.to_dict())
    return {"error": "Todo not found"}, 404

# POST (create new todo)
@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return {"error": "Task is required"}, 400
    
    new_todo = Todo(task=data["task"])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# PUT (update existing todo)
@app.route("/api/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    todo = db.session.get(Todo, id) # Todo.query.get(id) is legacy approach
    if not todo:
        return {"error": "Todo not found"}, 404
    
    data = request.get_json()
    if "task" in data:
        todo.task = data["task"]
    if "done" in data:
        todo.done = data["done"]

    db.session.commit()
    return jsonify(todo.to_dict())

# DELETE (remove a todo)
@app.route("/api/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = db.session.get(Todo, id) # Todo.query.get(id) is legacy approach
    if not todo:
        return {"error": "Todo not found"}, 404
    
    db.session.delete(todo)
    db.session.commit()
    return {"message": "Todo deleted successfully"}


if __name__ == "__main__":
    app.run(debug=True)