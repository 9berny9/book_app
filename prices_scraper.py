# import libraries
from bs4 import BeautifulSoup as bs
import requests


def get_search(search_term):
    """
    Generate url from search term
    """
    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


def get_book_url(book_href):
    template = 'https://www.amazon.com'
    book_url = template + book_href
    return book_url


def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
               'Accept-Language': 'en-US, en;q=0.5'}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
    return soup


def find_book(soup):
    book = soup.find_all('h2', {
        'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
    return book[0]


def get_title(book):
    book_title = book.find('a').text
    return book_title


def get_href(soup):
    book_href = soup.find('a')['href']
    return book_href


def get_description(soup):
    book_desc = soup.find_all('div', {'class':'a-expander-content a-expander-partial-collapse-content a-expander-content-expanded'})
    return book_desc[0].get_text()


search_book = get_search('tolkien')
search_page_soup = get_soup(search_book)
search_book = find_book(search_page_soup)
search_title = get_title(search_book)
search_href = get_href(search_book)
book_url = get_book_url(search_href)
book_soup = get_soup(book_url)
book_desc = get_description(book_soup)






