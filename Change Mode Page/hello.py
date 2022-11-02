import datetime
import json

from flask import Flask, render_template, request, make_response, session, url_for, redirect
from db_util import Database

app = Flask(__name__)
app.secret_key = "111"

app.permanent_session_lifetime = datetime.timedelta(days=365)

db = Database()


# метод для создания куки
@app.route("/add_cookie")
def add_cookie():
    resp = make_response("Add cookie")
    resp.set_cookie("test", "val")
    return resp


# метод для удаления куки
@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("Delete cookie")
    resp.set_cookie("test", "val", 0)


# реализация визитов
@app.route("/visits")
def visits():
    visits_count = session['visits'] if 'visits' in session.keys() else 0
    session['visits'] = visits_count + 1

    return f"Количество визитов: {session['visits']}"


# удаление данных о посещениях
@app.route("/delete_visits")
def delete_visits():
    session.pop('visits')
    return "ok"


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/films")
def films_list():
    country = request.args.get("country")
    rating = request.args.get('rating') or 0
    rating = float(rating)

    if rating and country:
        films = db.select(f"SELECT * FROM films WHERE UPPER(country) = UPPER('{country}') AND rating >= {rating};")
    elif country:
        films = db.select(f"SELECT * FROM films WHERE UPPER(country) = UPPER('{country}');")
    elif rating:
        films = db.select(f"SELECT * FROM films WHERE rating >= {rating};")
    else:
        films = db.select(f"SELECT * FROM films;")

    mode = request.cookies.get('mode') or 'light'
    context = {
        'films': films,
        'title': "FILMS",
        'country': country,
        'rating': rating,
        'style': mode
    }

    return render_template("films.html", **context)


@app.route('/film_form', methods=['GET', 'POST'])
def render_form():
    mode = request.cookies.get('mode') or 'light'
    if request.method == 'GET':
        return render_template('film_form.html', style=mode)

    name = request.form.get('name')
    rating = request.form.get('rating')
    country = request.form.get('country')

    if not (name and rating and country):
        return render_template("error.html", error="Одно из полей пустое!", page='film_form', style=mode)

    db.insert(f"INSERT INTO films (name, rating, country) VALUES ('{name}', {float(rating)}, '{country}');")

    response = f'Фильм "{name}" успешно добавлен'
    context = {
        'response': response,
        'style': mode
    }

    return render_template('film_form.html', **context)


@app.route("/film/<int:film_id>")
def get_film(film_id):
    mode = request.cookies.get('mode') or 'light'
    film = db.select(f"SELECT * FROM films WHERE id = {film_id}")

    if len(film):
        return render_template("film.html", title=film[0]['id'], film=film[0], style=mode)

    return render_template("error.html", error="Такого фильма не существует в системе")


@app.route('/change_mode')
def change_mode():
    mode = request.cookies.get('mode') or 'light'
    if mode == 'light':
        res = 'dark'
    else:
        res = 'light'

    resp = make_response(redirect_back())
    resp.set_cookie('mode', res)

    return resp


def redirect_back(default='films', **kwargs):
    """Функция для перехода на предыдущую страницу"""
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        return redirect(target)
    return redirect(url_for(default, **kwargs))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
