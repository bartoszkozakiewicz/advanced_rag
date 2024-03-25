from typing import Optional, List, Dict, Set
import re
import os
import json

from bs4 import BeautifulSoup
from tqdm import tqdm 

from scraping.scraper import Scraper

class MoreleNet:
    def __init__(self, url='https://www.morele.net', **scraper_kwargs):
        self.url = url
        self.categories : Optional[List[Dict]] = None
        self.categories_built = False
        self.product_list_pages_built = False
        self.product_urls_built = False

        self.cat_levels = {
            0: {'class': 'cn-departments-menu-item'},
            1: {'class': 'cn-row-menu-item-main'},
            2: {'class': 'cn-row-menu-item-nested'},
        }
        self.unique_urls : Dict[int, Set[str]] = {k: set() for k in range(len(self.cat_levels))}
        self.all_product_pages : Set[str] = set()
        self.product_urls : Set[str] = set()

        self.scraper = Scraper(**scraper_kwargs)

    def build_url(self, url):
        if url.startswith('http'):
            return url
        return self.url + url
        
    def build(self):
        self._init_categories()
        self._init_product_list_pages()
        self._init_product_urls()
        return self

    def _fetch_categories(self, soup, level=0):
        categories = soup.find_all('li', self.cat_levels[level])
        all_categories = []
        for i, category in enumerate(categories):
            cat_name = category.find('a').text.strip()
            cat_url = self.build_url(category.find('a').attrs['href'].strip())
            self.unique_urls[level].add(cat_url)
            # print(cat_name, cat_url, level)

            if level < max(self.cat_levels.keys()):
                if category.find('ul') is None:
                    sub_categories = None
                else:
                    sub_categories = self._fetch_categories(category.find('ul'), level+1)
            else:
                assert category.find('ul') is None, 'Category has subcategories but it should not'
                sub_categories = None
            all_categories.append({'category': cat_name, 'url': cat_url, 'subcategories': sub_categories})
        return all_categories
    
    def _init_categories(self):
        if self.categories_built:
            return
        
        resp = self.scraper.fetch(self.url)
        soup = BeautifulSoup(resp.text, 'lxml')

        categories = soup.find_all('div', {'class': 'cn-heading'})
        categories = [c for c in categories if c.text == 'KATEGORIE'][0]
        categories = categories.nextSibling.nextSibling
        assert categories.attrs['class'] == ['cn-window']

        categories = categories.find('div', {'class': 'cn-bar'}).find('ul', {'class': 'cn-current-departments'})

        self.categories = self._fetch_categories(categories, 0)
        self.categories_built = True

    def assert_categories_built(self):
        if not self.categories_built:
            raise ValueError('You need to build the object first')
    
    def get_unique_urls(self, level='all'):
        self.assert_categories_built()

        if level == 'all':
            return self.unique_urls
        else:
            return self.unique_urls[level]
    
    def get_categories(self):
        self.assert_categories_built()
        return self.categories
    
    def _init_product_list_pages(self):
        if self.product_list_pages_built:
            return

        self.assert_categories_built()
        all_urls = list(self.unique_urls[0]) + list(self.unique_urls[1]) + list(self.unique_urls[2])
        try:
            resp_generator = self.scraper.fetch_multiple(all_urls)
            for url, resp in tqdm(resp_generator, desc='Fetching product list pages', total=len(all_urls)):
                soup = BeautifulSoup(resp.text, 'lxml')
                pages = soup.find('ul', {'class': 'pagination dynamic'})
                if pages is None:
                    continue
                all_pages = pages.find_all('li')
                if len(all_pages) == 0:
                    all_pages = [url]
                else:
                    max_page = int(pages.attrs['data-count'])
                    base_href = all_pages[1].find('a').attrs['href']
                    all_pages = [re.sub('\d+/$', str(i), base_href) for i in range(1, max_page+1)]

                for p in all_pages:
                    self.all_product_pages.add(self.build_url(p))
            self.product_list_pages_built = True
        except:
            print(url)
            raise

    def assert_product_list_pages_built(self):
        if not self.product_list_pages_built:
            raise ValueError('You need to build the object first')

    def get_product_list_pages(self):
        self.assert_product_list_pages_built()
        return self.all_product_pages

    def _init_product_urls(self):
        if self.product_urls_built:
            return
        
        self.assert_product_list_pages_built()
        
        resp_generator = self.scraper.fetch_multiple(self.all_product_pages)
        for url, resp in tqdm(resp_generator, desc='Fetching product urls', total=len(self.all_product_pages)):
            soup = BeautifulSoup(resp.text, 'lxml')
            try:
                products = soup.find('div', {'class': 'cat-list-products'}).find_all('a', {'class': 'productLink'})
            except:
                print('ERROR FOR:', url)
                raise
            for p in products:
                self.product_urls.add(self.build_url(p['href']))

        self.product_urls_built = True

    def assert_product_urls_built(self):
        if not self.product_urls_built:
            raise ValueError('You need to build the object first')

    def get_product_urls(self):
        self.assert_product_urls_built()
        return self.product_urls
        
    def export_data(self, path):
        data = {
            'categories': self.categories,
            'unique_urls': {k: list(v) for k, v in self.unique_urls.items()},
            'all_product_pages': list(self.all_product_pages),
            'product_urls': list(self.product_urls),
        }
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, 'data.json'), 'w') as f:
            json.dump(data, f)

    def import_data(
            self, 
            categories=None,
            unique_urls=None,
            all_product_pages=None,
            product_urls=None,
            ):
        if categories:
            self.categories = categories
            self.categories_built = True
        if unique_urls:
            self.unique_urls = {int(k): set(v) for k, v in unique_urls.items()}
            self.categories_built = True
        if all_product_pages:
            self.all_product_pages = set(all_product_pages)
            self.product_list_pages_built = True
        if product_urls:
            self.product_urls = set(product_urls)
            self.product_urls_built = True
        return self
    
    def import_data_from_file(self, path):
        with open(os.path.join(path, 'data.json'), 'r') as f:
            data = json.load(f)
        self.import_data(**data)
        return self
        