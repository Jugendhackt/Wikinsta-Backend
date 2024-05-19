import time
from flask import Flask
import json
import threading
main_thread_running = True
import thefuzz.fuzz as fuzz
from wikipedia_search import search

app = Flask(__name__)
data: dict = {}

@app.route("/search/<art>")
def search(art):
    global data
    artis = data.keys()
    print(data)
    print(sorted([(a, fuzz.ratio(a,art)) for a in artis], key=lambda x: (-x[1], x[0])))
    sortedPairs = [art for art, _ in sorted([(a, fuzz.ratio(a,art)) for a in artis], key=lambda x: (-x[1], x[0]))]
    return sortedPairs


@app.route('/arti/<art>')
def get(art):
    info = data.get(art)
    if info != None:
        return data.get(art)
    else:
        return f"Keine Info zum Thema: {art}"


def search_wikipedia(art: str):
    #FIXME: WIKIPEDIA
    return search()

import keyboard
def exit_full():
    global main_thread_running
    main_thread_running = False
    exit()
keyboard.add_hotkey('ctrl + c', exit_full)
def update():
    global data
    while True:
        data = json.load(open("data.json", "r"))
        print("Re-cached database")
        for i in range(100):
            if not main_thread_running:
                return
            time.sleep(10/100)

if __name__ == "__main__":
    p = threading.Thread(target=update)
    p.start()
    app.run(host='0.0.0.0', port=5000)
