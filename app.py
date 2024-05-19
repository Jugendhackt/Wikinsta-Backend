import difflib
import random
import uuid

from flask import Flask
import json
import thefuzz.fuzz as fuzz
from articleExtractor import searchArticles

app = Flask(__name__)
data: dict = json.load(open("data.json", "r"))

def search_string_list(strings: list[str], match: str) -> list[str]:
    return [art for art, _ in sorted([(a, fuzz.ratio(a, match)) for a in strings], key=lambda x: (-x[1], x[0]))]
    #return difflib.get_close_matches(match,strings)

def add_article(art: dict):
    global data
    art.update({"uuid":str(uuid.uuid4())})
    data.update({str(uuid.uuid4()):art})
    json.dump(data,open("data.json","w"))
@app.route("/search/<art>")
def search(art):
    global data
    artis = data.keys()
    print(sorted([(a, fuzz.ratio(a,art)) for a in artis], key=lambda x: (-x[1], x[0])))
    return search_string_list(artis,art)


@app.route("/all/<amount>")
def all_artis(amount:int):
    global data
    artis = list(data.keys())
    return list(set(random.choices(artis,k=amount)))


@app.route('/by_title/<title>')
def get(title):
    info = {}
    for art in data.values():
        if art["title"] == title:
            info = art
    if info != {}:
        return info
    else:
        search_wikipedia(title)
        return get(title)

@app.route("/by_uuid/<uuid>")
def get_id(uuid):
    art = data.get(uuid)
    if art != None:
        return art
    else:
        return {}


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
    app.run(host='0.0.0.0', port=5000)
