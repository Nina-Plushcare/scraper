import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import json

from helpers.csv import CSVWriteHandler


class WebScraper:
    def __init__(self, page_id, confluence_url, username, api_token):
        self.page_id = page_id
        self.confluence_url = confluence_url
        self.username = username
        self.api_token = api_token
        self.csv_write_handler = CSVWriteHandler
        self.csv_write_handler.setup(file_path='data.csv')

    def get_links_from_toc(self, body: str):
        soup = BeautifulSoup(body, 'html.parser')
        toc = soup.find('ul', {'class': 'childpages-macro'})
        resources = []
        content = self.soup_to_csv(soup, resource_id=self.page_id)
        for link in toc.find_all('a'):
            resources.append(link.get('data-linked-resource-id')) if link.get(
                'data-linked-resource-type') == 'page' else None
        return content, resources

    def parse_links(self, resources):
        cont = []
        for resource in resources:
            data = self.scrape_data(f'https://accoladeinc.atlassian.net/wiki/api/v2/pages/{resource}?body-format=view')
            content = data.get('body').get('view').get('value')
            soup = BeautifulSoup(content, 'html.parser')
            content = self.soup_to_csv(soup, resource_id=resource)
            cont.append(content)
        print(cont)
        return cont

    def soup_to_csv(self, soup: BeautifulSoup, resource_id: int = None):
        content = {
            'resource_id': resource_id,
            'text': soup.text,
            'tag_stack': soup.tagStack
        }
        return content

    def scrape_data(self, confluence_link):
        auth = HTTPBasicAuth(self.username, self.api_token)
        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            "GET",
            confluence_link,
            headers=headers,
            auth=auth
        )
        val = json.loads(response.text)
        return val

    def run(self):
        data = self.scrape_data(self.confluence_url)
        content, resources = self.get_links_from_toc(data.get('body').get('view').get('value'))
        parsed_content = self.parse_links(resources)
        parsed_content.append(content)
        self.csv_write_handler.write(columns=['resource_id', 'text', 'tag_stack'], rows=parsed_content)
