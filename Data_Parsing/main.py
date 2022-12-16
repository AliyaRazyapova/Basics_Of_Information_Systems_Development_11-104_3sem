from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "111"


@app.route("/", methods=['POST', "GET"])
def main_list():
    url = "https://ria.ru/world/"
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')

    # titles
    titles = []
    kek = soup.find_all('a', class_="list-item__title color-font-hover-only")
    for i in range(len(kek)):
        titles.append(kek[i].text)

    # date
    dates = []
    kek = soup.find_all('div', class_="list-item__date")
    for i in range(len(kek)):
        dates.append(kek[i].text)

    # views
    views = []
    kek = soup.find_all('div', class_="list-item__views-text")
    for i in range(len(kek)):
        views.append(kek[i].text)
    all_1 = zip(titles, dates, views)

    return render_template("index.html", all=all_1)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
