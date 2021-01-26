from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_babel import gettext
from Website.models import Post
from Website import title, views
from Website.features.utils import (Weather, check_the_password, 
                                    get_the_emount_of_views, compare_pictures)
from Website.features.forms import (CheckPasswordForm, WeatherForm,
                                    ImageCompareForm)

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


@features.route("/compare_images", methods=['GET', 'POST'])
def compare_images():
    form = ImageCompareForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            picture_difference = compare_pictures(form)
            if picture_difference == 100:
                flash('Pictures are the same', 'success')
            else:
                flash(f'Pictures are {picture_difference}% simular', 'info')
        else:
            flash('You have entered wrong files. Files must be .png or .jpg', 'danger')
    return render_template('compare_images.html', title=gettext('Compare images'),
                           form=form)
