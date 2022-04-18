import streamlit as st
import book_rec as br
import re
import description_scraper as ds
import clearing as c
import requests
import pandas as pd
from PIL import Image
from io import StringIO


def header(data_b, data_r):
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.image('book_logo.png', width=300)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users", value=f"""{len(data_r.groupby('User-ID'))}""")
    col2.metric(label="Number of Books", value=f"""{len(data_b['ISBN'])}""")
    col3.metric(label="Number of Ratings", value=f"""{len(data_r['Book-Rating'])}""")


def book_rec_img(book_list_corr, column, column_number, number):
    book_corr_data = br.get_dataset_for_corr(br.dataset_base, book_list_corr[column_number])
    book_corr_name = book_corr_data['Book-Title']
    book_corr_author = book_corr_data['Book-Author']
    url_img = br.get_book_img(br.dataset_base, book_corr_name)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    column[number].image(book_cover, width=170,
                  caption=f'{book_corr_name} by {book_corr_author}')


def recommendation(book_list_corr):
    idx = 0
    for i in range(len(book_list_corr) - 1):
        cols = st.columns(3)

        if idx < len(book_list_corr) - 1:
            book_rec_img(book_list_corr, cols, idx, 0)
        idx += 1

        if idx < len(book_list_corr) - 1:
            book_rec_img(book_list_corr, cols, idx, 1)
        idx += 1
        if idx < len(book_list_corr) - 1:
            book_rec_img(book_list_corr, cols, idx, 2)
            idx = idx + 1
        else:
            break


def get_book_author(data, title):
    book_data = data[data['Book-Title'] == title]
    return book_data['Book-Author'].iloc[0]


def get_book_rating(data_low, title):
    book_data = data_low[data_low['Book-Title'] == title]
    book_rating = book_data.groupby('Book-Title').mean()
    return book_rating['Book-Rating'].mean()


def book_description(title, data, data_low):
    url_img = br.get_book_img(data, title)
    author = get_book_author(data, title)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    col1, col2 = st.columns((1, 2.5))
    col1.image(book_cover, width=170)
    col2.write(f"<b>{title}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{author}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{round(get_book_rating(data_low, title.lower()), 1)}/10</b>", unsafe_allow_html=True)
    soup_for_book = ds.get_soup_book(title)
    col2.write(ds.get_description(soup_for_book))


@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
def load_data(path):
    if path == "csv_files/BX-Books.csv":
        data = pd.read_csv(path, encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
    else:
        data = pd.read_csv(path, encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
        data = data[data['Book-Rating'] != 0]
    return data

@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
def get_books(data, searched_author):
    books_finding = data[data['Book-Author'].str.contains(searched_author.lower(), case=False, na=True,
                                                      flags=re.IGNORECASE, regex=False)]
    books_finding = books_finding.groupby('Book-Title').count().sort_values('User-ID', ascending=False).reset_index()
    return books_finding['Book-Title']


@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
def merge_books(ratings_base, books_base):
    return pd.merge(ratings_base, books_base, on=['ISBN'])

@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
def data_lower(data):
    return data.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)




if __name__ == "__main__":
    books = load_data("csv_files/BX-Books.csv")
    ratings = load_data("csv_files/BX-Book-Ratings.csv")
    header(books, ratings)
    dataset = merge_books(ratings, books)
    dataset_lowercase = data_lower(dataset)
    user_name = st.text_input("Enter your name:")
    if user_name:
        select_genres = st.multiselect("Select your favorite genres:", br.genres)
        if select_genres:
            publisher_language = st.selectbox("Select language for publishers:", c.publisher_languages().keys())
            if publisher_language:
                book_author = st.text_input("Select author's last name:")
                books_language = c.get_language(dataset, publisher_language)
                if book_author:
                    book_title = st.selectbox(f"Select book's name:", get_books(books_language, book_author))
                    check1, check2, check3 = st.columns(3)
                    description_box = check1.checkbox("Book description", value=False)
                    best_box = check2.checkbox("Best recommendations", value=False)
                    worst_box = check3.checkbox("Worst recommendations", value=False)
                    result = br.main(dataset_lowercase, book_title.lower(), book_author.lower())
                    if description_box:
                        st.markdown('#### Book description:')
                        book_description(book_title, dataset, dataset_lowercase)

                    if best_box:
                        st.markdown('#### Best recommendations:')
                        book_list_corr = result[0]['book'].head(10).to_list()
                        recommendation(book_list_corr)

                    if worst_box:
                        st.markdown('#### Worst recommendations:')
                        book_list_corr = result[0]['book'].tail(10).to_list()
                        recommendation(book_list_corr)


    #main(books, ratings)



