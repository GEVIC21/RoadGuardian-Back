from flask import Blueprint, jsonify
from flask_login import current_user, AnonymousUserMixin
from flask_restful import Api, Resource,reqparse
from flask_migrate import Migrate
from sqlalchemy import desc
import werkzeug
from charity.models import BlogPost, db
from werkzeug.utils import secure_filename
import os
from charity import app


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, "static/uploads")

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class BlogPostApi(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('libelle', type=str, required=True, help="This field cannot be left blank!",location='form')
    parser.add_argument('description', type=str, required=True, help="This field cannot be left blank!", location='form')
    parser.add_argument('categorie', type=str, required=True, help="This field cannot be left blank!", location='form')
    parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

    def post(self):
        data = BlogPostApi.parser.parse_args()
    

        image = data['image']
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    
            # Create the UPLOAD_FOLDER directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image.save(image_path)

            user_id = None
            if not isinstance(current_user._get_current_object(), AnonymousUserMixin):
               user_id = current_user.id

            blog_post = BlogPost(
                libelle=data['libelle'],
                description=data['description'],
                categorie=data['categorie'],
                image=image_filename,  # Store only the image filename in the database
                user_id=user_id
            )

            db.session.add(blog_post)
            db.session.commit()
            return {"message": "Blog post created successfully."}, 201
        
    def get(self):
        blog_posts = BlogPost.query.order_by(desc(BlogPost.date)).all()
        return jsonify([post.to_dict() for post in blog_posts])
    # Convert the BlogPost instance to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'libelle': self.libelle,
            'description': self.description,
            'categorie': self.categorie,
            'image': self.image
        }

    BlogPost.to_dict = to_dict

api.add_resource(BlogPostApi, '/blogpost')