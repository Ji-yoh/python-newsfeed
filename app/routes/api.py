import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()

    try: # attempt to create a new user w/ try..except
        # create a new user, bracket notation for Python dictionary is the same as dot notation in JS
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save in database
        db.add(newUser)
        db.commit()
    except:
        # insert failed, send error to frontend
        print(sys.exe_info()[0])
        db.rollback() # rollback on error
        return jsonify(message = 'Signup failed'), 500

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    # get user from database
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400
    
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True
    
    return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
@login_required # add login_required decorator
def comment():
    data = request.get_json() # get data from request
    db = get_db() # get database connection

    try: 
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newComment) # add to database
        db.commit() # commit changes
    except:
        print(sys.exc_info()[0])

        db.rollback() # rollback on error
        return jsonify(message = 'Comment failed'), 500
    
    return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT']) # adds a vote to a post by updating the Vote model
@login_required # add login_required decorator
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id & session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote) # add to database
        db.commit() # commit changes
    except:
        print(sys.exc_info()[0])

        db.rollback() # rollback on error
        return jsonify(message = 'Upvote failed'), 500
    
    return '', 204

@bp.route('/posts', methods=['POST']) # create a new post by adding a new record in the POST model
@login_required # add login_required decorator
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
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500
    
    return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT']) # update a post's title by id
@login_required # add login_required decorator
def update(id):
    data = request.get_json()
    db = get_db()

    try:
        # retrieve post & update title
        post = db.query(Post).filter(Post.id == id).one()
        post.title = data['title']
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404
    
    return '', 204

@bp.route('/posts/<id>', methods = ['DELETE']) # delete a post by id
@login_required # add login_required decorator
def delete(id):
    db = get_db()

    try:
        # delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404
    
    return '', 204
