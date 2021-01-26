from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from Website import db
from Website.models import Post
from Website.posts.forms import PostForm
from flask_babel import gettext
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(gettext(gettext('Your Post Has Been Created!')), 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title=gettext('New Post'),
                           form=form, legend=gettext('New Post'))


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(gettext('Your Post Has Been Updated!'), 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title=gettext('Update Post'),
                           form=form, legend=gettext('Update Post'))


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(gettext('Your Post Has Been Deleted!'), 'success')
    return redirect(url_for('main.home'))
