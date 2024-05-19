import difflib
import random
import uuid

from flask import Flask, Response
import json
import thefuzz.fuzz as fuzz
from articleExtractor import searchArticles

IP = "0.0.0.0"
PORT = 80


app = Flask(__name__)
data: dict = json.load(open("data.json", "r"))


# Returns a list which is ordered by similarity to a string
def search_string_list(strings: list[str], match: str) -> list[str]:
    return [art for art, _ in sorted([(a, fuzz.ratio(a, match)) for a in strings], key=lambda x: (-x[1], x[0]))]
    #return difflib.get_close_matches(match,strings)


# Adds an article to the db
def add_article(art: dict):
    global data
    art.update({"uuid":str(uuid.uuid4())})
    data.update({str(uuid.uuid4()):art})
    json.dump(data,open("data.json","w"))


# Searches articles
@app.route("/search/<art>")
def search(art: str):
    global data
    artis = list(data.keys())
    return search_string_list(artis,art)


# Gets a list of randomized articles from the db
@app.route("/random/<amount>")
def all_artis(amount: str):
    global data
    if not amount.isdigit():
        return Response(status="400")
    artis = list(data.keys())
    return list(set(random.choices(artis,k=int(amount))))


# Gets an article with a certain title from the db
# If none are available, it makes one
@app.route('/by_title/<title>')
def get(title: str):
    info = {}
    for art in data.values():
        if art["title"] == title:
            info = art
    if info != {}:
        return info
    else:
        search_wikipedia(title)
        return get(title)


# Gets an article vie UUID from the db
@app.route("/by_uuid/<uuid>")
def get_id(uuid: str):
    art = data.get(uuid)
    if art != None:
        return art
    else:
        return Response(status="404")


# Searches wikipedia for an article,
# which it then puts into the db
def search_wikipedia(name: str):
    global data
    response = searchArticles(name, "de")
    art = response[0]
    not_found = True
    for art2 in data.values():
        if art["title"] == art2["title"]:
            not_found = False
    if not_found:
        add_article(art)
    return art


if __name__ == "__main__":
    app.run(host=IP, port=PORT)
