import requests
import re
import streamlit as st
from backend import scraper
from PIL import Image
from pandas import DataFrame, Series
from backend.load_data import dataset, dataset_lowercase


def get_books(dataset_language: DataFrame, searched_author: str) -> Series:
    """
    Function returns books titles sorted by most rated.
    """
    books_finding = dataset_language[
        dataset_language.author.str.contains(
            searched_author.lower(), case=False, na=True, flags=re.IGNORECASE,
            regex=False)]
    books_finding = books_finding.groupby("title").count().sort_values(
        "id", ascending=False).reset_index()
    return books_finding.title


def book_description(title: str):
    """
    Function creates two columns with book image and description from request.
    """
    url_img = get_book_column(title, "image")
    author = get_book_column(title, column="author")
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    col1, col2 = st.columns((1, 2.5))
    col1.image(book_cover, width=170)
    col2.write(f"<b>{title}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{author}</b>", unsafe_allow_html=True)
    col2.write(
        f"<b>{round(get_rating(title.lower()), 1)}/10</b>",
        unsafe_allow_html=True)
    soup_for_book = scraper.get_soup_book(title)
    col2.write(scraper.get_description(soup_for_book))


def get_description(box: bool, book_title: str):
    """
    If the checkbox is true, It calls description function.
    """
    if box:
        st.markdown("#### Book description:")
        book_description(book_title)


def get_corr_df(title: str) -> Series:
    """
    Function returns series for title.
    """
    book_corr_data = dataset[dataset.title.str.lower() == title].iloc[0]
    return book_corr_data


def get_corr_img(df_corr: Series):
    """
    Function returns opened image from dataframe.
    """
    return Image.open(requests.get(df_corr.image, stream=True).raw)


def get_book_column(title: str, column: str) -> str:
    """
    Function returns Series for selected column.
    """
    book_data = dataset[dataset.title == title]
    return book_data[column].iloc[0]


def get_rating(title: str):
    """
    Function returns users average rating.
    """
    book_data = dataset_lowercase[dataset_lowercase.title == title]
    book_rating = book_data.groupby("title").mean()
    return book_rating.rating.mean()


def publisher_languages():
    """
    Language dict where value is first number in ISBN.
    """
    return {"English": ["0", "1"], "French": "2", "German": "3"}


def get_language(selected_language: str) -> DataFrame:
    """
    Function returns  dataframe with selected language.
    """
    language_condition = publisher_languages()
    language_condition = dataset[dataset.isbn.str.startswith(
        tuple(language_condition[selected_language]), na=False)]
    return language_condition


def get_genres():
    """
    List of genres.
    """
    genres_list = ["Art", "Business", "Chick-Lit", "Children's", "Christian",
                   "Classics", "Comedy", "Comics", "Contemporary",
                   "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction",
                   "Graphic Novels", "Historical Fiction", "History", "Horror",
                   "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction",
                   "Paranormal", "Philosophy", "Poetry", "Psychology",
                   "Religion", "Romance", "Science", "Science Fiction",
                   "Self Help", "Suspense", "Spirituality",
                   "Sports", "Thriller", "Travel", "Young Adult"]
    return genres_list


