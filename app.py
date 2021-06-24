import json
from flask import Flask, url_for
from bs4 import BeautifulSoup
import requests
from domain.FactCheck import FactCheck
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/')
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)
    return '<b>Factcheck API - Working</b><hr><br><br>Available endpoints:<br>' + json.dumps(links)


@app.route('/api/vrt', methods=['GET'])
def vrt():
    response = app.response_class(
        response=jsonFactChecksVrt,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/knack', methods=['GET'])
def knack():
    response = app.response_class(
        response=jsonFactChecksKnack,
        status=200,
        mimetype='application/json'
    )
    return response


def scrape_vrt():
    # List of factchecks that will be scraped
    factChecks = []
    # The url we are going to scrape (VRT NWS website)
    urlToScrape = 'https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/'
    # Sends a GET request to the page
    requestedPage = requests.get(urlToScrape).content.decode('utf8')

    # Create BeautifulSoup object with the content of the page request
    vrtFactCheckPage = BeautifulSoup(requestedPage, 'html.parser')
    # Get all blocks with the necessary info about the factchecks
    factCheckBlocks = vrtFactCheckPage.find_all(class_='vrt-teaser-wrapper')

    # We iterate through the blocks that have the factchecks content
    for block in factCheckBlocks:
        # This is the actual content with more info
        factCheckContent = block.find(class_='vrt-teaser__content-wrapper')
        # The title of the factcheck article
        title = factCheckContent.find(class_='vrt-teaser__title-text')
        # The description of the factcheck article
        description = factCheckContent.find(class_='vrt-teaser__subtitle')
        # The url of the factcheck article
        url = 'https://www.vrt.be' + block.find('a')['href']
        # The date of the factcheck article
        date = block.find('time')['datetime']
        try:
            title = title.text.replace('"', '')
            description = description.text
            # Create factcheck object
            factCheck = FactCheck(title, description, date, url, 'VRT', 'nl')
            # Add factcheck to the list
            factChecks.append(factCheck.__dict__)
        except:
            print("A factcheck block missed data.")

    # Return list with factchecks
    jsonFactChecks = json.dumps(factChecks, indent=4, ensure_ascii=False).encode('utf8')
    return jsonFactChecks.decode()


def scrape_knack():
    factChecksUrls = []
    factChecks = []
    # The url we are going to scrape (Knack website)
    urlToScrape = 'https://www.knack.be/nieuws/factcheck/'
    # Sends a GET request to the page
    requestedPage = requests.get(urlToScrape).content.decode('utf8')

    # Create BeautifulSoup object with the content of the page request
    knackFactCheckPage = BeautifulSoup(requestedPage, 'html.parser')
    # Will scrape all blocks with the necessary info about the factchecks
    factCheckBlocks = knackFactCheckPage.find_all(class_='rmgTeaser-content')

    # We iterate through the blocks
    for block in factCheckBlocks:
        # The url of the factcheck article
        # We remove the first 2 characters because the href has two '//' for some reason
        url = block.find('a')['href'][2:]
        # Check if url contains the word factcheck, to avoid adding irrelevant other urls
        if url.__contains__("factcheck"):
            factChecksUrls.append('https://' + url)

    for url in factChecksUrls:
        # The url we are going to scrape (Knack website)
        fullArticleUrl = url

        # Sends a GET request to the page
        fullArticlePage = requests.get(fullArticleUrl).content.decode('utf8')
        knackFactCheckPage = BeautifulSoup(fullArticlePage, 'html.parser')

        # Scrape the title
        title = knackFactCheckPage.find(class_="rmgDetail-title m-altTitle").text
        title = title.lstrip()
        title = title.rstrip()
        title = title.replace("\n", "")

        # Scrape the date
        date = knackFactCheckPage.find(class_="rmgDetail-main").find('li').text
        date = date.rstrip()
        date = date.lstrip()
        date = date[:8]

        # Scrape the description
        description = knackFactCheckPage.find(class_="rmgDetail-intro").text

        # Make factcheck object
        factCheck = FactCheck(title, description, date, url, 'KNACK', 'nl')

        print("Scraping factcheck", title, "\n")
        factChecks.append(factCheck.__dict__)

    jsonFactChecks = json.dumps(factChecks, indent=4, ensure_ascii=False).encode('utf8')
    return jsonFactChecks.decode()


jsonFactChecksVrt = scrape_vrt()
jsonFactChecksKnack = scrape_knack()

if __name__ == '__main__':
    app.run()
