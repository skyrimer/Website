import os
import secrets
from PIL import Image, ImageDraw
from flask import url_for, current_app, flash, request
from flask_mail import Message
from Website import mail, bcrypt
from Website.models import User, Post
from pyshorteners import Shortener


def my_login(form):
    user = User.query.filter_by(email=form.email_or_username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        return user
    user = User.query.filter_by(username=form.email_or_username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        return user


def get_user_and_his_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    for post in posts.items:
        all_text, first_paragraph = post.content, post.content.split('\r')[0]
        if first_paragraph != all_text:
            post.content = first_paragraph + "........"
    return user, posts


def save_picture(form_picture):
    def prepare_mask(size, antialias=2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.ANTIALIAS)

    def crop(im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0:
            im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0:
            im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.ANTIALIAS)

    random_hex = secrets.token_hex(8)
    f_ext = '.png'
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pictures',
                                picture_fn)

    size = (150, 150)
    im = Image.open(form_picture)
    im = crop(im, size)
    im.putalpha(prepare_mask(size, 4))
    im.save(picture_path, 'png')
    return picture_fn

def reset_password(email):
    user = User.query.filter_by(email=email).first()
    try:
        send_reset_email(user)
    except:
        flash('Something went wrong. Please, contact developers!',
              'warning')
    else:
        flash('An email has been sent with instructions to reset your password.',
          'info')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender="KirillsWebsite@gmail.com",
                  recipients=[user.email])
    shortner = Shortener()
    msg.body = f'''To reset your password, visit the following link:

{shortner.tinyurl.short(url_for('users.reset_token', token=token, _external=True))}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
