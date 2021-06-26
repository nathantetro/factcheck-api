from dal import factCheckRepository
from business import factCheckScraper
from util.consoleColors import colors


def init_factchecks(initDatabase=False):
    factChecksToAdd = []
    print(
        colors.BOLD + colors.OKBLUE + "===================== SCRAPING VRT FACTCHECKS =====================" + colors.BOLD + colors.OKBLUE)
    factChecksToAdd.extend(factCheckScraper.scrape_vrt_factchecks())
    print(
        colors.BOLD + colors.OKBLUE + "===================== SCRAPING KNACK FACTCHECKS =====================" + colors.BOLD + colors.OKBLUE)
    factChecksToAdd.extend(factCheckScraper.scrape_knack_factchecks())
    if len(factChecksToAdd) >= 1:
        factCheckRepository.create_factcheck_bulk(factChecksToAdd, initDatabase)


def get_all_factchecks():
    return factCheckRepository.read_all_factchecks()


def get_factcheck_from_publisher(publisher):
    return factCheckRepository.read_factchecks_of_publisher(publisher)
