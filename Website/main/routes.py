from flask import (render_template, request, Blueprint, redirect,
                   url_for, flash, make_response)
from Website.models import Post
from Website import title, db, babel, languages, views
from Website.main.forms import FeedbackForm
from Website.models import Feedback
from flask_login import current_user, login_required
from flask_babel import gettext, refresh
main = Blueprint('main', __name__)


@main.route("/")
@views.count
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title=title)


@main.route("/about")
def about():
    return render_template('about.html', title=gettext('About me'))


@main.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if current_user.is_authenticated:
        form = FeedbackForm()
        if request.method == "POST" and form.validate_on_submit:
            feedback = Feedback(content=form.feedback_text.data,
                                _user=current_user)
            db.session.add(feedback)
            db.session.commit()
            form.feedback_text.data = None
            flash(gettext('Thank you for yor opinion!)'), 'success')
    else:
        form = None
    page = request.args.get('page', 1, type=int)
    opinions = Feedback.query.order_by(Feedback.date_posted.desc())\
                       .paginate(page=page, per_page=5)
    return render_template('feedback.html', title=gettext('Feedback'),
                           form=form, opinions=opinions)


@main.route('/languages/<string:language>')
def change_language(language):

    @babel.localeselector
    def get_locale():
        if language in languages:
            return language
        else:
            return request.accept_languages.best_match(languages)
    if current_user.is_authenticated:
        current_user.language = get_locale()
        db.session.commit()
    refresh()
    return redirect(request.referrer)


@main.route('/change_theme')
@login_required
def change_theme():
    if current_user.theme == 'light':
        current_user.theme = 'dark'
    else:
        current_user.theme = 'light'
    db.session.commit()
    return redirect(request.referrer)


@main.route("/best_of_the_best_in_the_world")
def show_the_best():
    return redirect('https://vk.com/berry_0107')
