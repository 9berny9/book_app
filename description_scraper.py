# import libraries
from bs4 import BeautifulSoup as bs
import requests
import re

def get_search(search_term):
    """
    Generate url from search term
    """
    template = 'https://www.goodreads.com/search?q={}'
    search_term = re.sub(r'[^\w]', ' ', search_term)
    url = search_term.replace(' ', '+')
    return template.format(url)


def get_book_url(book_href):
    template = 'https://www.goodreads.com'
    book_url = template + book_href
    return book_url


def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
               'Accept-Language': 'en-US, en;q=0.5'}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
    return soup


def find_book(soup):
    book = soup.find_all('td')
    return book[0]


def get_title(book):
    book_title = book.find('a').text
    return book_title


def get_href(soup):
    book_href = soup.find('a')['href']
    return book_href


def get_description(soup):
    book_description = soup.find('div', id="description")
    book_description = book_description.find_all('span')
    return book_description[1].text

def main(book_title):
    search_book = get_search(book_title)
    print(search_book)
    search_page_soup = get_soup(search_book)
    search_book = find_book(search_page_soup)

    #search_title = get_title(search_book)
    search_href = get_href(search_book)
    book_url = get_book_url(search_href)
    book_soup = get_soup(book_url)
    book_desc = get_description(book_soup)
    return book_desc




