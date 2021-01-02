from flask import (render_template, url_for, flash, redirect,
                   request, Blueprint, abort)
from flask_login import login_user, current_user, logout_user, login_required
from Website import db, bcrypt
from Website.models import User, Post
from Website.users.forms import (RegistrationForm, LoginForm,
                                 UpdateAccountForm, RequestResetForm,
                                 ResetPasswordForm, ChangePasswordForm)
from Website.users.utils import (save_picture, reset_password,
                                 my_login, get_user_and_his_posts)
from flask_babel import gettext
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    bio=form.bio.data, password=hashed_password)
        if user.email == 'chekmenev2004@mail.ru':
            user.admin = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(gettext('Your Account Has Been Created!'), 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title=gettext('Register'), form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form=form)
    if form.validate_on_submit() and my_login(form):
        login_user(my_login(form), remember=form.remember.data)
        flash('Login successful', 'success')
        return redirect(url_for('main.home'))
    else:
        flash(gettext('Login Unsuccessful. Please Check Email and Password'), 'danger')
    return render_template('login.html', title=gettext('Login'), form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account/<string:username>", methods=['GET', 'POST'])
def account(username):
    form = UpdateAccountForm()
    if request.method == 'GET':
        if (current_user.is_authenticated) and (current_user.username == username):
            user = current_user
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.bio.data = current_user.bio
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                form = None
            else:
                abort(404)
    elif form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('users.account', username=current_user.username))
    image_file = url_for('static',
                         filename='profile_pictures/' + user.image_file)
    return render_template('account.html', title=gettext('Account'),
                           image_file=image_file,
                           form=form, user=user)


@users.route("/user/<string:username>")
def user_posts(username):
    user, posts = get_user_and_his_posts(username)
    return render_template('user_posts.html',
                           posts=posts,
                           user=user,
                           title=f"{user.username}'s posts")


@users.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            current_user.password = bcrypt.generate_password_hash(form.new_password.data)\
                                          .decode('utf-8')
            db.session.commit()
            flash(gettext('The password has been changed successfully!'), 'success')
            return redirect(url_for('main.home'))
        return render_template('change_password.html',
                                title=gettext('Change Password'),
                                form=form)
    else:
        return redirect(url_for('main.home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        reset_password(form.email.data)
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title=gettext('Reset Password'),
                           form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(gettext('That is an invalid or expired token'), 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(gettext('Your password has been updated! You are now able to log in'),
              'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title=gettext('Reset Password'),
                           form=form)
