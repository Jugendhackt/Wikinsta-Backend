# Import the lib for Web-Requests
import requests

# Article Format:
# {
#  'category': <category>,
#  'lang': <language_code>,
#  'title': <title>
#  'id': <ID of the Wikipedia Article>
#  'summary': <A "small" summary>,
#  'picture': <none | {
#   'img': <link>,
#   'license': <license>,
#   'artist': <artist>
#  }>
# }

# Function to get some informations about a Wikipedia article.

def getRandomArticle(language_code):
    response = requests.get(f"https://{language_code}.wikipedia.org/wiki/Special:Random")
    return searchArticles(response.url.split('/')[-1], language_code)

def searchArticles(search_query='Never gonna give you up', language_code='en'):
    url = f'https://{language_code}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={search_query}'
    response = requests.get(url)
    jsonResponse = response.json()

    articles = []

    for id, value in jsonResponse['query']['pages'].items():
        img = getImage(value['title'], language_code)

        if 'missing' not in value:
            articles.append({
                'lang': language_code,
                'category': 'other',
                'title': value['title'],
                'id': id,
                'summary': value['extract'],
                'picture': img
            })

    return articles

# Returns an Image in form of {'img': <the picture link>, 'license': <the license>}

def getImage(search_query='Never gonna give you up', language_code='en'):
    url = f'https://{language_code}.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_query}'
    response = requests.get(url)
    jsonResponse = response.json()

    imgs = []

    for id, value in jsonResponse['query']['pages'].items():
        if 'original' in value:
            imgs.append(value['original']['source'])
        else:
            imgs.append('noimg')

    img = imgs[0]

    if img != 'noimg':
        license = getLicense(img, language_code)
        if license.startswith("cc") or license == 'public domain':
            return {'img': img, 'license': getLicense(img, language_code), 'artist': getArtist(img, language_code)}

    return None

# Returns the License Short form of an image

def getLicense(imgURL, language_code='en'):
    imgName = imgURL.split('/')[-1]

    url = f'https://{language_code}.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&format=json&titles=File%3a{imgName}'
    response = requests.get(url)
    jsonResponse = response.json()

    # query > pages > -1 > imageinfo > [0] > extmetadata > LicenseShortName > value
    shortLicenses = []

    for id, value in jsonResponse['query']['pages'].items():
        shortLicenses.append(value['imageinfo'][0]['extmetadata']['LicenseShortName']['value'])

    return shortLicenses[0].lower()

# Returns the Artist of the given Image

def getArtist(imgURL, language_code='en'):
    try:
        imgName = imgURL.split('/')[-1]

        url = f'https://{language_code}.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&format=json&titles=File%3a{imgName}'
        response = requests.get(url)
        jsonResponse = response.json()

        return jsonResponse['query']['pages']['-1']['imageinfo'][0]['extmetadata']['Artist']['value']
    except KeyError:
        return 'No Artist found'