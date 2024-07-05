from flask import Flask, abort, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, current_user, logout_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, User, Todo
from forms import RegisterForm, LoginForm, TodoForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text} - {error}", 'danger')
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(
            content=form.content.data,
            priority=form.priority.data,
            user_id=current_user.id
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('dashboard'))

    sort_by = request.args.get('sort_by', 'priority')
    if sort_by == 'date_created':
        todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created.desc()).all()
    else:
        todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.priority.desc()).all()

    return render_template('dashboard.html', form=form, todos=todos, sort_by=sort_by)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if todo.author != current_user:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = Todo.query.get_or_404(id)
    if todo.author != current_user:
        abort(403)
    
    form = TodoForm()
    if form.validate_on_submit():
        todo.content = form.content.data
        todo.priority = form.priority.data
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.content.data = todo.content
        form.priority.data = todo.priority

    return render_template('update.html', form=form, todo=todo)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
