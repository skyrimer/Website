from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_babel import gettext
from Website.models import Post
from Website import title, views
from Website.features.utils import Weather, check_the_password, get_the_emount_of_views
from Website.features.forms import CheckPasswordForm, WeatherForm

features = Blueprint('features', __name__)

@features.route('/features')
@views.count
def my_features():
    my_views = get_the_emount_of_views()
    word = gettext("Something I can do")
    word_length = len(word)
    return render_template('features.html',
                           title=gettext("Features"),
                           my_views=my_views,
                           word=word,
                           word_length=word_length)


@features.route('/password_check', methods=['GET', 'POST'])
def password_check():
    form = CheckPasswordForm()
    if form.validate_on_submit():
        result = check_the_password(form.check_field.data)
        flash(*result)
        return redirect(url_for('main.home'))
    else:
        return render_template('password_check.html',
                               title=gettext('Password check'), form=form)


@features.route('/weather', methods=['GET', 'POST'])
def weather():
    form = WeatherForm()
    if form.validate_on_submit():
        city = form.city.data
        weather_at_place = Weather(city)
    else:
        weather_at_place = Weather('Zug')
    return render_template('weather.html', title=gettext('Weather'),
                           weather=weather_at_place,
                           form=form)
                    
@features.route('/rocket', methods=['GET', 'POST'])
def rocket():
    return render_template('rocket.html', title=gettext('Rocket Fly'))

@features.route('/password_generator', methods=['GET', 'POST'])
def password_generator():
    return render_template('password_generator.html', title=gettext('Password Generator'))


@features.route('/face_recognition')
def face_recognition():
    return render_template('face_recognition.html', title=gettext('Face Recognotion'))