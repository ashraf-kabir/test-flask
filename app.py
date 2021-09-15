from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_flask.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content:
            flash('You must enter some content!')
            return redirect(url_for('index'))

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Your task has been added!')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('There was an issue adding your task')
            return redirect(url_for('index'))
    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('index.html', tasks=tasks)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            flash('Task Updated')
            return redirect(url_for('index'))
            # return redirect('/')
        except:
            db.session.rollback()
            flash('There was an issue updating the task')
            return redirect(url_for('update'))
            # return 'There was an issue updating the task'
    else:
        return render_template('update.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    if not task:
        # return 'No task found'
        flash('No task found')
        return redirect(url_for('index'))
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully')
        return redirect(url_for('index'))
        # return redirect('/')
    except:
        db.session.rollback()
        flash('There was an issue deleting the task')
        return redirect(url_for('index'))
        # return 'There was an issue deleting the task'


if (__name__ == '__main__'):
    app.run(debug=True)