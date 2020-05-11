from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
DBURI = 'postgres://dbuser:zubur1@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = DBURI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


@app.route('/todos/create', methods=['POST'])
def create():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })


# main method
if __name__ == '__main__':
    app.run(host='192.168.1.200', port='8000', debug=True)
