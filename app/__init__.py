from flask import Flask
from app.models import db
from app.main import bp, init_app as init_login
import os

def create_app():
    app = Flask(__name__)
    
    # Use file-based SQLite database bundled with the app
    db_path = os.path.join(app.root_path, 'blueberry_blog.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    
    db.init_app(app)
    app.register_blueprint(bp)
    init_login(app)

    with app.app_context():
        db.create_all()
        # Pre-populate with fancy posts if empty
        from app.models import User, Post, Comment
        if not User.query.first():
            demo_user = User(username='blueberry_admin')
            demo_user.set_password('blueberry123')
            db.session.add(demo_user)
            db.session.commit()
            posts = [
                Post(title='Welcome to Blueberry Blog!', content='This is your first taste of the juiciest blog on the web. 🍇', author=demo_user),
                Post(title='A Splash of Color', content='Blueberries are not just tasty, they are beautiful! Enjoy our vibrant new theme.', author=demo_user),
                Post(title='Why Blogging is Like Making Jam', content='It takes time, love, and the right ingredients. Start your own post today!', author=demo_user),
            ]
            db.session.add_all(posts)
            db.session.commit()
            # Add demo comments
            comment1 = Comment(content='Love the new look! 💙', user=demo_user, post=posts[0])
            comment2 = Comment(content='Blueberries are my favorite!', user=demo_user, post=posts[1])
            db.session.add_all([comment1, comment2])
            db.session.commit()

    return app