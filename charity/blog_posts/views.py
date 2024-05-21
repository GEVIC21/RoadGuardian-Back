import os
from flask import abort, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from charity import app
from charity import db
from charity.models import BlogPost
from charity.blog_posts.forms import BlogPostForm
import os
from flask import flash, redirect, render_template, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from charity.blog_posts.forms import BlogPostForm
from charity.models import BlogPost, db

from flask import send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, "static/uploads")
# UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")


blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        image = form.image.data
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    
            # Create the UPLOAD_FOLDER directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image.save(image_path)

            blog_post = BlogPost(
                libelle=form.libelle.data,
                description=form.description.data,
                categorie=form.categorie.data,
                image=image_filename,  # Store only the image filename in the database
                user_id=current_user.id
            )

            db.session.add(blog_post)
            db.session.commit()
            flash("Blog Post Created")
            return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)

@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',libelle=blog_post.libelle,
                            date=blog_post.date,post=blog_post
    )

@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.libelle = form.libelle.data
        blog_post.description = form.description.data
        blog_post.categorie = form.categorie.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.libelle.data = blog_post.libelle
        form.description.data = blog_post.description
        form.categorie.data = blog_post.categorie
    return render_template('create_post.html', title='Update',
                           form=form)

@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('D:/BACK_END/FLASK/Tutos2/charity/blog_posts/static/uploads', filename)