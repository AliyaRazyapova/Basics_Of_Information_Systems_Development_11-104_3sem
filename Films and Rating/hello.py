# необходимые импорты
import json
from flask import *

# инициализируем приложение
# из документации:
#     The flask object implements a WSGI application and acts as the central
#     object.  It is passed the name of the module or package of the
#     application.  Once it is created it will act as a central registry for
#     the view functions, the URL rules, template configuration and much more.
app = Flask(__name__)


def get_():
    with open("films.json", "r") as file:
        films = json.load(fp=file)
    return films


def set_(new_films):
    with open("films.json", "w") as file:
        json.dump(obj=new_films, fp=file)


FILMS = get_()


# перенаправляет с / на /films
@app.route("/")
def redirect_():
    return redirect("/films")

# дальше реализуем методы, которые мы можем выполнить из браузера,
# благодаря указанным относительным путям


def rating_filt(films, rating: float):
    filt = []
    for film in films:
        if not film['rating'] < rating:
            filt.append(film)
    return filt


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/films")
def films_list():
    # читаем файл с фильмами
    # with open("films.json", 'r') as f:
    #     films = json.load(f)
    films = FILMS

    # получаем GET-параметр country (Russia/USA/French
    country = request.args.get("country")
    minim = request.args.get("rating")

    if minim:
        films = rating_filt(films, rating=float(minim))

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS",
        'country': country
    }

    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)


# метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # читаем файл
    # with open("films.json", 'r') as f:
    #     films = json.load(f)

    # ищем нужный нам фильм и возвращаем шаблон с контекстом
    for film in FILMS: #изменено
        if film['id'] == film_id:
            return render_template("film.html", title=film['name'], film=film)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")


@app.get("/films/add")
def add_get():
    return render_template("add.html")


@app.post("/films/add")
def add_post():
    form_data = request.form.to_dict()
    film = {
        "id": len(FILMS),
        "name": form_data['name'],
        "rating": float(form_data['rating']),
        "country": form_data['country']
    }
    FILMS.append(film)
    set_(FILMS)
    return render_template("add.html", status="Фильм добавлен")


if __name__ == "__main__":
    app.run()
