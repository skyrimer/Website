from flask import url_for, current_app
from flask_babel import gettext
from pyowm import OWM
from pyowm.commons.exceptions import (NotFoundError,
                                      InvalidSSLCertificateError,
                                      APIResponseError)
from Website import pyowm_key
from password_strength import PasswordStats
from Website import views, db
from sqlalchemy.sql import select
from skimage.metrics import structural_similarity as ssim
from cv2 import cvtColor, COLOR_BGR2GRAY, imread, resize
from werkzeug.utils import secure_filename
import os
class Weather():
    def __init__(self, city):
        owm = OWM(pyowm_key)
        mgr = owm.weather_manager()
        try:
            observation = mgr.weather_at_place(city)
        except InvalidSSLCertificateError:
            self.status = None
        except APIResponseError:
            self.status = None
        except NotFoundError:
            self.status = 1
        else:
            self.status = 2
            weather = observation.weather
            self.detailed_status = gettext(weather.detailed_status.capitalize())
            temperature = weather.temperature('celsius')
            self.temperature = round(temperature['temp'], 1)
            self.wind = weather.wind()['speed']
            self.humidity = weather.humidity
            self.heat_index = weather.heat_index
            self.clouds = weather.clouds
            self.city = city
            self.weather_icon = url_for('static',
                                        filename=f'weather_icons/{weather.status}.png')


def check_the_password(password):
    password = int(round(PasswordStats(password).strength(), 2) * 100)
    if password < 33:
        prefix = 'The password is week - '
        strength_color = 'danger'
    elif password < 66:
        prefix = 'The password is Ok - '
        strength_color = 'info'
    else:
        prefix = 'The password is strong - '
        strength_color = 'success'
    return f"{prefix}{password}%", strength_color

def get_the_emount_of_views():
    user_counter = []
    my_views = db.engine.execute(select([views.requests]))
    for view in my_views:
        if view.user_agent not in user_counter:
            user_counter.append(view.user_agent)
    return len(user_counter)


def compare_pictures(form):

    def save_images(form):

        path_1 = os.path.join(current_app.root_path,
                                    'static\\profile_pictures', form.image_1.name)
        path_2 = os.path.join(current_app.root_path,
                                    'static\\profile_pictures', form.image_2.name)
        form.image_1.data.save(path_1)
        form.image_2.data.save(path_2)
        return path_1, path_2 

    def delete_images(path_1, path_2):
        os.remove(path_1)
        os.remove(path_2)

    path_1, path_2 = save_images(form)
    # resize in case the dimensions are different
    image_1 = resize(imread(path_1), (500, 500))
    image_2 = resize(imread(path_2), (500, 500))

    image_1 = cvtColor(image_1, COLOR_BGR2GRAY)
    image_2 = cvtColor(image_2, COLOR_BGR2GRAY)

    delete_images(path_1, path_2)
    return int(ssim(image_1, image_2) * 100)
