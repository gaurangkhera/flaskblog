from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Blog, Comment, Like
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
        flash('Blog deleted successfully.', category='success')

    return redirect(url_for('views.viewblogs'))

@views.route('/blogs/update/<title>', methods=['GET', 'POST'])
@login_required
def edit_blog(title):
    blog = Blog.query.filter_by(title=title).first()
    if request.method == "POST":
        new_title = request.form.get('new_title')
        new_content = request.form.get('new_content')
        if not blog:
            flash("Cannot find blog.", category='error')
        elif current_user.username != blog.author:
            flash("You do not have permission to edit this blog.", category='error') 
        else:  
            blog.title = new_title
            blog.content = new_content
            db.session.add(blog)
            db.session.commit()
            flash('Blog updated successfully.', category='success')

    return render_template('edit.html', blog=blog)

@views.route('/blogs/comment/<title>', methods=['GET', 'POST'])
@login_required
def comment(title):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        blog = Blog.query.filter_by(title=title).first()
        if Blog:
            comment = Comment(
                text=text, author=current_user.username, blog=blog.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Blog does not exist.', category='error')

    return redirect(url_for('views.viewblogs'))

@views.route('/blogs/deletecmnt/<text>')
def delete_cmnt(text):
    comment = Comment.query.filter_by(text=text).first()

    if not comment:
        flash('Cannot find comment.', category='error')
    elif current_user.username != comment.author:
        flash('You do not have permission to delete this comment.', 'error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully.', 'success')

    return redirect(url_for('views.viewblogs'))

@views.route('/blogs/likeblog/<title>')
@login_required
def like(title):
    blog = Blog.query.filter_by(title=title).first()

    if not blog:
        flash('Blog not found.', 'error')
    else:
        like = Like(blog_id=blog.id)
        db.session.add(like)
        db.session.commit()
        flash(f"Thank you for liking {blog.author}'s post.", 'success')
    return redirect(url_for('views.viewblogs'))



