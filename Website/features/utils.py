from flask import url_for
from flask_babel import gettext
from pyowm import OWM
from pyowm.commons.exceptions import (NotFoundError,
                                      InvalidSSLCertificateError,
                                      APIResponseError)
from Website import pyowm_key
from password_strength import PasswordStats
from Website import views, db
from sqlalchemy.sql import select

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