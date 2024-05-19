import difflib
import random
from flask import Flask
import json
main_thread_running = True
import thefuzz.fuzz as fuzz
from articleExtractor import searchArticles

app = Flask(__name__)
data: dict = json.load(open("data.json", "r"))

def search_string_list(strings: list[str], match: str) -> list[str]:
    # return [art for art, _ in sorted([(a, fuzz.ratio(a, match)) for a in strings], key=lambda x: (-x[1], x[0]))]
    return difflib.get_close_matches(match,strings)

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


@app.route('/arti/<art>')
def get(art):
    info = data.get(art)
    if info != None:
        return data.get(art)
    else:
        search_wikipedia(art)
        return get(art)


def search_wikipedia(art: str):
    global data
    response = searchArticles(art,"en")
    arti = response[0]
    title = arti["title"]

    if data.get(title) == None:
        data.update({title:arti})
    json.dump(data,open("data.json","w"))
    return arti["summary"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
