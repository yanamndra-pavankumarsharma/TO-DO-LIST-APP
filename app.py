from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        new_todo = Todo(title=todo_title, desc=todo_desc)
        db.session.add(new_todo)
        db.session.commit()
        return redirect("/")

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

# Delete Functionality
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Update Functionality
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('base.html', todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
