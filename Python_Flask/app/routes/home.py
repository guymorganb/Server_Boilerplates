from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db  # import the get_db function from app

bp = Blueprint('home', __name__, url_prefix='/')


# As shown in the preceding example, we import the functions Blueprint() and render_template() from the Flask module.
# Blueprint() lets us consolidate routes onto a single bp object that the parent app can register later.
# This corresponds to using the Router middleware of Express.js.
# We then define two new functions: index() and login().
# In each case, we add a @bp.route() decorator before the function to turn it into a route.
@bp.route('/')
def index():
    # get all posts
    db = get_db()
    posts = (
        db
        .query(Post)
        .order_by(Post.created_at.desc())
        .all()
    )

    return render_template(  # render the template with posts data
        'homepage.html',
        posts=posts,
        loggedIn=session.get('loggedIn')  # passing the logged-in session to the template
    )


@bp.route('/login')
def login():
    # not logged in yet
    if session.get('loggedIn') is None:
        return render_template('login.html')

    return redirect('/dashboard')


# the <id> route parameter in the decorator function that becomes a function parameter in the single() function.
# We can use that parameter to query the database for a specific post.


@bp.route('/post/<id>')
def single(id):
    # get single post by id
    db = get_db()
    post = (db.query(Post).filter(Post.id == id).one())  # this is the query to the db

    # render single post template
    return render_template(
        'single-post.html',
        post=post,  # post is part of the template engine views and is being rendered in the browser
        loggedIn=session.get('loggedIn')
    )
# This time, we use the filter() method on the connection object to specify the SQL WHERE clause,
# and we end by using the one() method instead of all().
# We then pass the single post object to the single-post.html template.
# Once the template is rendered and the response sent, the context for this route terminates,
# and the teardown function closes the database connection.
