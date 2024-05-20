import requests

def addRandomArticlesToData(count):
    for i in range(count):
        response = requests.get(f"https://de.wikipedia.org/wiki/Special:Random")
        title = response.url.split('/')[-1]

        requests.get(f'http://localhost:5000/create_title/{title}')

        print(f'Finished {i+1}. random Article')

if __name__ == '__main__':
    addRandomArticlesToData(10)