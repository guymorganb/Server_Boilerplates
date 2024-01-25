from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# This time, using the url_prefix argument, we prefix every route in the blueprint with /dashboard.
# The routes thus become /dashboard and /dashboard/edit/<id> when registered with the app.


# allows dashboard posts
@bp.route('/')
@login_required   # Yes, you can stack decorators!
def dash():
    db = get_db()
    posts = (   # Without the parentheses, this would throw an indentation error.
        db.query(Post)
        .filter(Post.user_id == session.get('user_id'))
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template(
        'dashboard.html',
        posts=posts,
        loggedIn = session.get('loggedIn')
    )

# edit post on dashboard
@bp.route('/edit/<id>')
@login_required    # Yes, you can stack decorators!
def edit(id):
    # get single post by id
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()

    #render edit page
    return render_template(
        'edit-post.html',
        post=post,
        loggedIn = session.get('loggedIn')
    )
