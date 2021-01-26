from flask import (render_template, url_for, flash, redirect,
                   request, Blueprint, abort)
from flask_login import (login_user, current_user, logout_user,
                         login_required)
from Website import (db, bcrypt, google, languages,
                     google_blueprint, github_blueprint)
from Website.models import User, Post, OAuth, Feedback
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from Website.users.forms import (RegistrationForm, LoginForm,
                                 UpdateAccountForm, RequestResetForm,
                                 ResetPasswordForm, ChangePasswordForm)
from Website.users.utils import (save_picture, reset_password,
                                 my_login, get_user_and_his_posts,
                                 get_picture_from_url)
from flask_babel import gettext
from secrets import token_hex
users = Blueprint('users', __name__)
google_blueprint.backend = SQLAlchemyStorage(
    OAuth, db.session, user=current_user)
github_blueprint.backend = SQLAlchemyStorage(
    OAuth, db.session, user=current_user)


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
        user.check_for_admin()
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
    if form.validate_on_submit():
        user_from_form = my_login(form)
        if user_from_form:
            login_user(user_from_form, remember=form.remember.data)
            flash('Login successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(
                gettext('Login Unsuccessful. Please Check Email and Password'), 'danger')
    return render_template('login.html', title='Log in', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been loged out!', 'info')
    return redirect(url_for('main.home'))


@users.route("/delete_user", methods=['GET', 'POST'])
@login_required
def delete_user():
    user = User.query.filter_by(id=current_user.id).first()
    posts = Post.query.filter_by(author=current_user)
    opinions = Feedback.query.filter_by(_user=current_user)
    for post in posts:
        db.session.delete(post)
    for opinion in opinions:
        db.session.delete(opinion)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your account was successfuly deleted', 'danger')
    return redirect(url_for('main.home'))


#! Google registration
@users.route("/google_authorize")
def google_auth():
    if not current_user.is_authenticated:
        return redirect(url_for("google.login"))
    flash('You are already logged in', 'info')
    return redirect(url_for('main.home'))


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):

    account_info = blueprint.session.get("/oauth2/v1/userinfo")

    if account_info.ok:
        account_info_json = account_info.json()

        user = User.query.filter_by(email=account_info_json['email']).first()

        if not user:
            hashed_password = bcrypt.generate_password_hash(token_hex(16))\
                .decode('utf-8')
            image_file = get_picture_from_url(account_info_json['picture'])
            user = User(username=account_info_json['name'],
                        email=account_info_json['email'],
                        password=hashed_password,
                        image_file=image_file)
            user.check_for_admin()
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Login successful", 'info')


#! GitHub registration
@users.route("/github_authorize")
def github_auth():
    if not current_user.is_authenticated:
        return redirect(url_for("github.login"))
    flash('You are already logged in', 'info')
    return redirect(url_for('main.home'))


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):

    account_info = blueprint.session.get("/user")

    if account_info.ok:
        account_info_json = account_info.json()

        user = User.query.filter_by(email=account_info_json['email']).first()

        if not user:
            hashed_password = bcrypt.generate_password_hash(token_hex(16))\
                .decode('utf-8')
            image_file = get_picture_from_url(account_info_json['avatar_url'])
            user = User(username=account_info_json['name'],
                        email=account_info_json['email'],
                        password=hashed_password,
                        image_file=image_file)
            user.check_for_admin()
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Login successful", 'info')


@users.route("/account/<string:username>", methods=['GET', 'POST'])
def account(username):
    form = UpdateAccountForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        if user:
            if (current_user.is_authenticated) and (current_user.username == user.username):
                form.username.data = user.username
                form.email.data = user.email
                form.bio.data = user.bio
            else:
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
        flash(gettext('Your Account Has Been Updated!'), 'success')
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
