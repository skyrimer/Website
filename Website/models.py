from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, redirect, url_for, flash
from Website import db, login_manager, admin
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    user_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text(), default='Too lazy to make bio')
    posts = db.relationship('Post', backref='author', lazy=True)
    opinion = db.relationship('Feedback', backref='_user', lazy=True)
    language = db.Column(db.String(3), nullable=False, default='en')
    theme = db.Column(db.String(5), nullable=False, default='light')

    def check_for_admin(self):
        if self.email in os.environ['MY_EMAIL'].split():
            self.user_admin = True

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.title}', '{self.date_posted}')"


class AdminViewer(ModelView):
    form_base_class = SecureForm
    action_disallowed_list = ['delete']
    edit_template = 'admin_edit.html'
    create_template = 'admin_create.html'
    list_template = 'admin_list.html'
    can_create = False

    def is_accessible(self):
        try:
            return current_user.user_admin
        except:
            return None

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash('You need to be registerd and admin have permition to enter this page', 'warning')
        return redirect(url_for('users.login'))


admin.add_view(AdminViewer(User, db.session))
admin.add_view(AdminViewer(Post, db.session))
admin.add_view(AdminViewer(Feedback, db.session))
