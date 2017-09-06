#!/usr/bin/python
import argparse
import re
import sys

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from bs4 import BeautifulSoup


class ResultParcel(object):
    def __init__(self, owner, address, parcel, url):
        self.owner = owner.strip()[:15]
        self.address = re.sub(r'\s+', ' ', address.strip())
        self.parcel = parcel.strip()
        self.url = self.clean_url(url)

    def __repr__(self):
        return '{} {} {} {}'.format(self.owner, self.address, self.parcel, self.url)

    @staticmethod
    def clean_url(url):
        return url.split('&')[0]

    @property
    def is_vacant_land(self):
        return not bool(re.search(r'\d+\s+', self.address))

    @property
    def street(self):
        if self.is_vacant_land:
            return self.address
        return re.search(r'\d+\s+(.+)', self.address).group(1)


class AuditorCrawl(object):
    ROOT_URL = 'http://oh-mahoning-auditor.publicaccessnow.com/'
    SEARCH_URL = ROOT_URL + 'OwnerSearch.aspx'

    result_parcels = []
    cookie = None
    exclude_land = False

    def __init__(self, owner, no_vacant_land):
        self.owner = owner
        self.exclude_land = no_vacant_land

    def crawl(self):
        # Get pages
        page_links, self.cookie = self.do_search(self.owner)

        for link in page_links:
            self.get_page(link)

        self.result_parcels.sort(key=lambda x: x.street)

        self.do_output()

    def do_search(self, query):

        body = """
------WebKitFormBoundaryd2z3cZYy5JIXFGLR
Content-Disposition: form-data; name="owner"

%s

------WebKitFormBoundaryd2z3cZYy5JIXFGLR
Content-Disposition: form-data; name="SearchType"

1

------WebKitFormBoundaryd2z3cZYy5JIXFGLR
Content-Disposition: form-data; name="btnSearch"
""" % query

        headers = {
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryd2z3cZYy5JIXFGLR'
        }

        # First page
        request = Request(self.SEARCH_URL, body, headers)
        response = urlopen(request)

        soup = BeautifulSoup(response.read(), 'html.parser')

        pages = soup.findAll(class_='pagination')[0].findAll('a')[2:-1]

        page_links = [page['href'] for page in pages]
        cookie = ('C_owner', query)

        self.process_page(soup)

        return page_links, cookie

    def get_page(self, url):
        cookies = {'Cookie', '{}={}'.format(self.cookie[0], self.cookie[1])}
        request = Request(self.SEARCH_URL + url, headers=cookies)
        response = urlopen(request)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.process_page(soup)

    def process_page(self, soup):
        rows = soup.findAll('tr', class_='searchResult')
        for row in rows:
            self.result_parcels.append(
                ResultParcel(
                    owner=row.contents[1].text,
                    address=row.contents[5].text,
                    parcel=row.contents[3].text,
                    url=row.contents[3].contents[0]['href']
                )
            )

    def do_output(self):
        structure_count = 0
        vacant_land_count = 0
        for result in self.result_parcels:
            if result.is_vacant_land:
                vacant_land_count += 1
            else:
                structure_count += 1

        filtered_results = self.result_parcels

        if self.exclude_land:
            filtered_results = [x for x in filtered_results if not x.is_vacant_land]

        # Table formatting.
        max_owner = max([len(p.owner) for p in filtered_results]) + 10
        max_address = max([len(p.address) for p in filtered_results]) + 10
        max_parcel = max([len(p.parcel) for p in filtered_results]) + 6
        max_url = max([len(p.url) for p in filtered_results]) + 31
        header = 'Owner%sAddress%sParcel%sUrl' % (
            ' ' * (max_address - 10), ' ' * (max_parcel + 0), ' ' * (max_url - 17)
        )

        sys.stdout.write('\nResults for "{}": {} Structures {} Lots\n\n'
                         .format(self.owner, structure_count, vacant_land_count))
        sys.stdout.write(header + '\n')
        sys.stdout.write('-' * len(header) + '\n')

        for result in filtered_results:
            owner_output = result.owner + ' ' * (max_owner - len(result.owner))
            address_output = result.address + ' ' * (max_address - len(result.address))
            parcel_output = result.parcel + ' ' * (max_parcel - len(result.parcel))
            sys.stdout.write(
                '%s%s%s%s\n' % (owner_output, address_output, parcel_output, result.url)
            )


def main():
    parser = argparse.ArgumentParser(description="Auditor owner search.")
    parser.add_argument('owner', type=str)
    parser.add_argument('--no-vacant-land', dest='no_vacant_land', action='store_true',
                        default=False, help='Exclude vacant land')
    args = parser.parse_args()

    crawler = AuditorCrawl(args.owner, args.no_vacant_land)
    crawler.crawl()

if __name__ == '__main__':
    main()
