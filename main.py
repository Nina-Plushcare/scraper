from helpers.scraper import WebScraper

PAGE_ID = 1459224598
CONFLUENCE_URL = f'https://accoladeinc.atlassian.net/wiki/api/v2/pages/{PAGE_ID}?body-format=view'
USERNAME = ''
API_TOKEN = ''

if __name__ == '__main__':
    scraper = WebScraper(PAGE_ID, CONFLUENCE_URL, USERNAME, API_TOKEN)
    scraper.run()

