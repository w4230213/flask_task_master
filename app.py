from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    owner = db.Column(db.String(50), nullable=False, default='John Doe')
    date_created = db.Column(db.DateTime, default=datetime.today)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_contet = request.form['content']
        owner = request.form['owner']
        new_task = Task(content=task_contet, owner=owner)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/index')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue updating this task'
    else:
        return render_template('update.html', task=task)


@app.route('/done/<int:id>')
def done(id):
    task = Task.query.get_or_404(id)

    try:
        task.completed = True
        db.session.commit()
        return redirect('/index')
    except:
        return 'There was an issue when finishing this task.'

if __name__ == '__main__':
    app.run(debug=True)
