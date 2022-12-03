from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Blog
from . import db


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("index.html")

@views.route('/blogpost', methods=['GET', 'POST'])
@login_required
def blog():
    if request.method == 'POST':
        blog_title = request.form.get('blog_title')
        blog_content = request.form.get('blog_content')

        blog_title_exists = Blog.query.filter_by(title=blog_title).first()
        if blog_title_exists:
            flash('There is already a blog with this title.', category='error')
        elif len(blog_title) == 0:
            flash("Blog title cannot be empty.", category='error')
        elif len(blog_content) == 0:
            flash('Blog cannot be empty.', category='error')
        else:
            new_blog = Blog(title=blog_title, content=blog_content, author=current_user.username)
            db.session.add(new_blog)
            db.session.commit()
            flash('Blog posted successfully.', category='success')
    return render_template('postblogs.html')

@views.route('/blogs')
def viewblogs():
    allBlogs = Blog.query.all()
    return render_template('blogs.html', allBlogs=allBlogs)

@views.route('/blogs/delete/<title>')
@login_required
def delete_blog(title):
    blog = Blog.query.filter_by(title=title).first()

    if not blog:
        flash("Cannot find blog.", category='error')
    elif current_user.username != blog.author:
        flash('You do not have permission to delete this blog.', category='error')
    else:
        db.session.delete(blog)
        db.session.commit()
        flash('Post deleted successfully.', category='success')

    return redirect(url_for('views.home'))