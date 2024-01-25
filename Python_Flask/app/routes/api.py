# This is where we'll define all the API endpoints for the app.
import sqlalchemy
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys
from app.utils.auth import login_required
bp = Blueprint('api', __name__, url_prefix='/api')


# JavaScript uses req.body to access incoming POST data,
# Flask, differs a bit. Remember, Flask creates a context for every request,
# and these contexts understand which values on the global 'g' object are unique to them.
# Well, you can use another global contextual object that contains information about
# the request itself—the request object. Like the g object, you need to import it first.


@bp.route('/users', methods=['POST'])  # adding a POST route: will resolve to /api/users
def signup():
    data = request.get_json()
    db = get_db()  # brining in the database

    # noinspection PyBroadException
    try:
        newUser = User(  # take in user data to pass to the User model for creating an account
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        # save in the database
        db.add(newUser)
        db.commit()
        print('success!')
        session.clear()  # handle the user session: clear any existing session, and set up a new session
        session['user_id'] = newUser.id
        session['loggedIn'] = True
        return jsonify(id=newUser.id)  # return the newly created users id

    except AssertionError:  # these are just to demonstrate different variations of error handling
        print('validation error')
    except sqlalchemy.exc.IntegrityError:
        print('mysql error')
    except:
        print(sys.exe_info()[0])
        # insert failed, so rollback database, so its connection isn't stuck open and send error to front end
        db.rollback()
        # insert failed, send error to the front end
        return jsonify(message='Signup failed'), 500



    # AttributeError: 'dict' object has no attribute 'username'
    # We verified that data had a username property,
    # so why did the error occur? The answer is that data isn't an object in the traditional JavaScript sense.
    # It's a Python dictionary, which is a different data type altogether.
    # To access the properties of a dictionary, we must use bracket notation (for example, data['property']).


@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204


@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    try:
        user = db.query(User).filter(User.email == data['email']).one()
        if not user.verify_password(data['password']):
            return jsonify(message = 'Incorrect Password'), 400
        session.clear()
        session['user_id'] = user.id
        session['loggedIn'] = True

        return jsonify(id = user.id)
    except:
        print(sys.exc_info()[0])
        return jsonify(message='Incorrect credentials'), 400

# Keep in mind that if db.commit() fails, the connection will remain in a pending state.
# This doesn't seem to have any negative effects during local testing.
# You can try to sign up again on the front end, and the next attempt will go through just fine.
# In a production environment, however, those pending database connections can result in app crashes.


# Comment route: Because this is a POST route,
# we can capture the posted data by using the get_json()
# method and create a new comment by using the returned dictionary.
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    data = request.get_json()
    db = get_db()
    try:
        # create new comment: The comment_text and post_id values come
        # from the front end, but the session stores the user_id value.
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )
        db.add(newComment)
        db.commit()
    except:
        print(sys.exe_info()[0])

        db.rollback()
        return jsonify(message = 'Comment failed'), 500
    return jsonify(id = newComment.id)


# PUT route for upvotes
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
    data = request.get_json()
    db = get_db()
    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exe_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote Failed'), 500

    return '', 204


# create new post
@bp.route('/posts', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    db = get_db()
    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
    except:
        print(sys.exe_info()[0])

        db.rollback()
        return jsonify(message = 'Pst failed'), 500

    return jsonify(id = newPost.id)


# update a post
@bp.route('/posts/<id>', methods=['PUT'])
# You'll use an <id> route parameter again and capture the parameter in the
# update() function. You'll use that id to perform the update.
@login_required
def update(id):
    data = request.get_json()
    db = get_db()
# The data variable is a dictionary—hence, the bracket notation of data['title'].
# The post variable, contrastingly, is an object created from the User class—so it uses dot notation.
    try:
        post = db.query(Post).filter(Post.id == id).one()
        post.title = data['title']
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204


# delete post
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()

    try:
        #delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204


# Note the following example of Python code:
#
# Copy
# food = {
#   'name': 'banana',
#   'calories': 105
# }
# This syntax would create an object in JavaScript, but in Python, it creates a dictionary.
# Python creates objects only from classes, meaning that you need to use something like food = Food('banana').
# However, it makes sense to create a food object only if it needs methods attached to it.
# Otherwise, the dictionary is the better data type to use.
