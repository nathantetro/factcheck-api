import requests
from bs4 import BeautifulSoup
from domain.FactCheck import FactCheck
from util.consoleColors import colors
from datetime import datetime


def scrape_vrt_factchecks():
    # List of factchecks that will be scraped
    factChecks = []
    # The url we are going to scrape (VRT NWS website)
    urlToScrape = 'https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/'
    # Sends a GET request to the page
    requestedPage = requests.get(urlToScrape).content.decode('utf8')

    print(colors.BOLD + colors.OKGREEN + 'Scraping VRT factchecks...' + colors.ENDC)

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
        thumbnail = block.find('img')['data-src'][2:]
        try:
            title = title.text.replace('"', '')
            description = description.text
            # Create factcheck object
            factCheck = FactCheck(title, description, datetime.strptime(date[:10], '%Y-%m-%d'), url, 'VRT', 'nl',
                                  thumbnail)
            # Add factcheck to the list
            factChecks.append(factCheck)
        except Exception as error:
            print(colors.FAIL + "A VRT website element could not be scraped." + colors.ENDC)

    return factChecks


def scrape_knack_factchecks():
    factChecksUrls = []
    factChecks = []
    # The url we are going to scrape (Knack website)
    urlToScrape = 'https://www.knack.be/nieuws/factcheck/'
    # Sends a GET request to the page
    requestedPage = requests.get(urlToScrape).content.decode('utf8')

    print(colors.BOLD + colors.OKGREEN + 'Scraping Knack factchecks...' + colors.ENDC)

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
        try:
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

            # Scrape thumbnail
            thumbnail = knackFactCheckPage.find(class_="u-sm-100vw")['src']

            # Make factcheck object
            factCheck = FactCheck(title, description, datetime.strptime(date, '%d/%m/%y'), url, 'KNACK', 'nl',
                                  thumbnail)

            factChecks.append(factCheck)
        except Exception as error:
            print(error)
            print(colors.FAIL + "A Knack website element could not be scraped. \n Error: " + str(error) + colors.ENDC)

    return factChecks
