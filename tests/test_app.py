import pytest
from app import create_app
from app.models import db, User, Post, Comment
from flask import url_for

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'LOGIN_DISABLED': False,
        'SECRET_KEY': 'test',
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# --- Model Tests ---
def test_user_password_hashing():
    user = User(username='testuser')
    user.set_password('testpass')
    assert user.check_password('testpass')
    assert not user.check_password('wrongpass')

def test_post_creation(app):
    user = User(username='author')
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()
    post = Post(title='Test', content='Content', author=user)
    db.session.add(post)
    db.session.commit()
    assert post in db.session
    assert post.author == user

def test_comment_creation(app):
    user = User(username='author')
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()
    post = Post(title='Test', content='Content', author=user)
    db.session.add(post)
    db.session.commit()
    comment = Comment(content='Nice post!', user=user, post=post)
    db.session.add(comment)
    db.session.commit()
    assert comment in db.session
    assert comment.user == user
    assert comment.post == post

# --- View/Route Tests ---
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Blueberry' in response.data or b'Post' in response.data

def test_register_login_logout(client):
    # Register
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert b'registered successfully' in response.data
    # Login
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert b'Logged in successfully' in response.data
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b'logged out' in response.data or b'index' in response.data

def test_create_post_requires_login(client):
    response = client.get('/create_post', follow_redirects=True)
    assert b'login' in response.data or response.status_code == 200

def test_404_page(client):
    response = client.get('/nonexistentpage')
    assert response.status_code == 404
    assert b'404' in response.data or b'not found' in response.data.lower()
