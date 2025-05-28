# /home/devops/code/my-new-flask-project/app/main.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import db, User, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

# --- Flask-Login ---
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Set the login view
login_manager.session_protection = "strong" # Security measure

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Routes ---

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('main.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash("Title and content are required", "error")
            return redirect(url_for('main.create_post'))

        new_post = Post(title=title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_post.html')

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must be logged in to comment.', 'error')
            return redirect(url_for('main.login'))
        content = request.form.get('content')
        if not content or not content.strip():
            flash('Comment cannot be empty.', 'error')
        else:
            comment = Comment(content=content.strip(), user=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('main.view_post', post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created_at.desc()).all()
    return render_template('view_post.html', post=post, comments=comments)

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'error')
        return redirect(url_for('main.view_post', post_id=post.id))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('main.edit_post', post_id=post.id))
        post.title = title
        post.content = content
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))
    return render_template('edit_post.html', post=post)


# --- Error handling ---
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- Initialize Flask-Login in the app factory---
def init_app(app):
    login_manager.init_app(app)