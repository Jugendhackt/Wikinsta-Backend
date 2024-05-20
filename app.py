import difflib
import random
import uuid
import sys

import textdistance
from flask import Flask, Response
from flask_cors import CORS, cross_origin
import json
import thefuzz.fuzz as fuzz
from articleExtractor import searchArticles
import textdistance as td

IP = "0.0.0.0"
PORT = 5000


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
data: dict = json.load(open("data.json", "r"))


# Returns a list which is ordered by similarity to a string
def search_string_list(strings: list[str], match: str) -> list[str]:
    print([(a, textdistance.hamming.normalized_similarity(a, match)) for a in strings])
    return [
        art for art, sim in
        sorted
        ([(a, textdistance.hamming.normalized_similarity(a, match)) for a in strings],key=lambda x: (-x[1], x[0]))
        if sim > 0
    ]
    #return [art for art, _ in sorted([(a, fuzz.ratio(a, match)) for a in strings], key=lambda x: (-x[1], x[0]))]
    #return difflib.get_close_matches(match,strings)

print("sims",search_string_list(["Holz","Baum","Wasser"],"elon musk"))

# Adds an article to the db
def add_article(art: dict):
    global data
    art.update({"uuid":str(uuid.uuid4())})
    data.update({str(uuid.uuid4()):art})
    json.dump(data,open("data.json","w"))


# Searches articles
@app.route("/search/<title>")
def search(title: str):
    global data
    artis = list(data.values())
    s = search_string_list([art["title"] for art in artis],title)
    return s


# Gets a list of randomized articles from the db
@app.route("/random/<amount>")
def all_artis(amount: str):
    global data
    if not amount.isdigit():
        return Response(status="400")
    artis = list(data.values())

    return random.choices(artis, k=int(amount))


# Gets an article with a certain title from the db
# If none are available, it makes one
@app.route('/create_title/<title>')
def create_title(title: str):
    return search_wikipedia(title)


# Gets an article vie UUID from the db
@app.route("/by_uuid/<uuid>")
def get_uuid(uuid: str):
    art = data.get(uuid)
    if art != None:
        return art
    else:
        return Response(status="404")

# Gets an article via normal id from the db
@app.route("/by_id/<id>")
def get_id(id: str):
    article = find(list(data.values()), lambda art: art["id"] == id)
    if not article is None:
        return article
    else:
        return Response(status="404")

# Searches wikipedia for an article,
# which it then puts into the db
def search_wikipedia(name: str):
    global data
    response = searchArticles(name, "de")
    if len(response) == 0:
        return {}
    art = response[0]
    not_found = True
    for art2 in data.values():
        if art["title"] == art2["title"]:
            not_found = False
    if not_found:
        add_article(art)
    return art

def find(iterable, predicate):
    if len(iterable) == 0:
        return None

    if predicate(iterable[0]):
        return iterable[0]

    return find(iterable[1:], predicate)


if __name__ == "__main__":
    with open("./content/tabelle_musik.csv", "r") as f:
        music_lines = f.read().splitlines()

    try:
        mode = sys.argv[1]
    except:
        mode = "server"

    match mode:
        case "server":
            app.run(host=IP, port=PORT)
        case "data":
            for line in music_lines:
                title = line.split(',')[0]
                print(f"Adding {title}")
                search_wikipedia(title)

