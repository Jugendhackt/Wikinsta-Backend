# Import the lib for Web-Requests
import requests

# Function to get some informations about a Wikipedia article.

def searchArticles(language_code='en', search_query='Never gonna give you up'):
    url = f'https://{language_code}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={search_query}'
    response = requests.get(url)
    jsonResponse = response.json()

    articles = []

    for id, value in jsonResponse['query']['pages'].items():
        articles.append({
            'lang': language_code,
            'title': value['title'],
            'id': id,
            'summary': value['extract']
        })

    return articles