# Import necessary modules from Flask, Flask-RESTful, and SQLAlchemy
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application instance
app = Flask(__name__)

# Create an Api instance to handle RESTful API requests
api = Api(app)

# Configure the SQLite database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

# Define a model for the Video table
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(100), nullable=False)  # Name column, non-nullable
    views = db.Column(db.Integer, nullable=False)  # Views column, non-nullable
    likes = db.Column(db.Integer, nullable=False)  # Likes column, non-nullable

    # String representation of the model
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# Define request parser and arguments for PUT request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

# Define request parser and arguments for PATCH request
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

# Define resource fields for marshalling output
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Define Video resource
class Video(Resource):
    # GET request to retrieve a video by ID
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()  # Query video by ID
        if not result:
            abort(404, message="Could not find video with that id")  # Abort if video not found
        return result  # Return video if found

    # PUT request to create a new video
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()  # Parse arguments
        result = VideoModel.query.filter_by(id=video_id).first()  # Check if video ID already exists
        if result:
            abort(409, message="Video id taken...")  # Abort if video ID exists

        # Create new video entry
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)  # Add video to the session
        db.session.commit()  # Commit the session
        return video, 201  # Return the created video and HTTP status 201

    # PATCH request to update an existing video
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()  # Parse arguments
        result = VideoModel.query.filter_by(id=video_id).first()  # Query video by ID
        if not result:
            abort(404, message="Video doesn't exist, cannot update")  # Abort if video not found

        # Update video attributes if provided in the request
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()  # Commit the changes
        return result  # Return the updated video

    # DELETE request to delete a video by ID
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)  # Abort if video ID doesn't exist
        del videos[video_id]  # Delete video from the dictionary
        return '', 204  # Return empty response and HTTP status 204

# Add the Video resource to the API with the URL route /video/<int:video_id>
api.add_resource(Video, "/video/<int:video_id>")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
