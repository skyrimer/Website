from flask import render_template, request, Blueprint, redirect, url_for, flash
from Website.models import Post
from Website import title, db, babel, languages
from Website.main.forms import FeedbackForm
from Website.models import Feedback
from flask_login import current_user
from flask_babel import gettext, refresh
main = Blueprint('main', __name__)


@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=5)
    for post in posts.items:
        all_text, first_paragraph = post.content, post.content.split('\r')[0]
        if first_paragraph != all_text:
            post.content = first_paragraph + "........"
    return render_template('home.html', posts=posts, title=title)


@main.route("/about")
def about():
    return render_template('about.html', title=gettext('About me'))


@main.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if current_user.is_authenticated:
        form = FeedbackForm()
        if request.method == "POST" and form.validate_on_submit:
            feedback = Feedback(title=form.title.data,
                                content=form.feedback_text.data,
                                _user=current_user)
            db.session.add(feedback)
            db.session.commit()
            form.feedback_text.data = None
            flash(gettext('Thank you for yor opinion!)'), 'success')
    else:
        form = None
    opinions = Feedback.query.order_by(Feedback.date_posted.desc())
    return render_template('feedback.html', title=gettext('Feedback'),
                           form=form, opinions=opinions)


@main.route('/languages/<string:language>')
def change_language(language):

    @babel.localeselector
    def get_locale():
        if language in languages:
            flash(gettext(f'Language was changed'), 'success')
            return language
        else:
            flash(gettext('No such language supported'), 'warning')
            return request.accept_languages.best_match(languages)

    refresh()
    return redirect('/')


@main.route("/best_of_the_best_in_the_world")
def show_the_best():
    return redirect('https://vk.com/berry_0107')
