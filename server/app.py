from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Create Flask application

app = Flask(__name__)
CORS(app)

# Configure database URI and other settings


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize SQLAlchemy


DB = SQLAlchemy(app)

# Initialize migrations


migrate = Migrate(app, DB)


# Create a Post model that represents a database table for storing posts


class Post(DB.Model):

    # PRIMARY KEY
    id = DB.Column(DB.Integer, primary_key=True)

    # TITLE COLUMN
    title = DB.Column(DB.String(100), nullable=False)

    # CONTENT COLUMN
    content = DB.Column(DB.Text, nullable=False)


# Route 1:
# Fetch all posts

@app.route('/posts', methods=['GET'])
def fetch_posts():

    # FETCH EVERYTHING FROM DATABASE
    data = Post.query.all()

    # EMPTY LIST
    results = []

    # LOOP THROUGH EACH POST
    for post in data:

        # APPEND EACH POST AS A DICTIONARY
        results.append({
            'id': post.id,
            'title': post.title,
            'content': post.content
        })

    # RETURN JSON RESPONSE
    return jsonify(results), 200


# Route 2:
# Add new post


@app.route('/add-post', methods=['POST'])
def add_post():

    # GET DATA FROM REQUEST BODY
    data = request.get_json()

    # CREATE NEW POST OBJECT
    new_post = Post(
        title=data['title'],
        content=data['content']
    )

    # SAVE TO DATABASE
    DB.session.add(new_post)
    DB.session.commit()

    return jsonify({
        'message': 'Post added successfully'
    }), 201


# Route 3:
# Fetch single post by ID

@app.route('/posts/<int:id>', methods=['GET'])
def fetch_single_post(id):

    # GET POST BY ID
    post = Post.query.get(id)

    # CHECK IF POST EXISTS
    if post is None:
        return jsonify({
            'message': 'Post not found'
        }), 404

    # RETURN POST DATA
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content
    }), 200


# Route 4:
# Update existing post


@app.route('/update-post/<int:id>', methods=['PATCH'])
def update_post(id):

    # FIND POST
    post = Post.query.get(id)

    # CHECK IF POST EXISTS
    if post is None:
        return jsonify({
            'message': 'Post not found'
        }), 404

    # GET UPDATED DATA
    data = request.get_json()

    # UPDATE VALUES
    post.title = data['title']
    post.content = data['content']

    # SAVE CHANGES
    DB.session.commit()

    return jsonify({
        'message': 'Post updated successfully'
    }), 200

# Route 5:
# Delete a post by ID

@app.route('/delete-post/<int:id>', methods=['DELETE'])
def delete_post(id):

    # FIND POST
    post = Post.query.get(id)

    # CHECK IF POST EXISTS
    if post is None:
        return jsonify({
            'message': 'Post not found'
        }), 404

    # DELETE POST
    DB.session.delete(post)
    DB.session.commit()

    return jsonify({
        'message': 'Post deleted successfully'
    }), 200


# RUN APPLICATION


if __name__ == '__main__':
    app.run(debug=True)