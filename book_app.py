import streamlit as st
import requests
import re
from backend import scraper
from PIL import Image
from backend.book_rec import recommender
from backend.load_data import books, ratings, dataset, dataset_lowercase, \
    NUMBER_OF_RECOMMENDATIONS


def run_app():
    read_style()
    header()
    genres = user_select()
    language = language_select(genres)
    df = language_dataframe(language)
    author = author_select(df)
    title = title_select(author, df)
    if title:
        # create three check columns
        check1, check2, check3 = st.columns(3)
        description_box = check1.checkbox("Book description", value=False)
        best_box = check2.checkbox("Best recommendations", value=False)
        worst_box = check3.checkbox("Worst recommendations", value=False)
        # final dataset with corr
        df_corr = recommender(title.lower(), author.lower())
        # create boxes
        get_description(description_box, title)
        get_rec(df_corr, best_box, worst_box)


def read_style():
    with open("src/style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def header():
    st.image("src/book_logo.png", width=300)
    # create three columns abreast
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users",
                value=f"{len(ratings.groupby('User-ID'))}")
    col2.metric(label="Number of Books",
                value=f"{len(books['ISBN'])}")
    col3.metric(label="Number of Ratings",
                value=f"{len(ratings['Book-Rating'])}")


def user_select():
    user_name = st.text_input("Enter your name:")
    if user_name:
        select_genres = st.multiselect("Select your favorite genres:",
                                       get_genres())
        return select_genres


def language_select(selected_genres):
    if selected_genres:
        publisher_language = st.selectbox("Select publisher's language:",
                                          publisher_languages().keys())
        return publisher_language


def language_dataframe(selected_language):
    if selected_language:
        df_language = get_language(selected_language)
        return df_language


def author_select(df):
    if df is not None:
        author = st.text_input("Select author's last name:")
        return author


def title_select(selected_author, df):
    if selected_author:
        title = st.selectbox(f"Select book's name:",
                             get_books(df, selected_author))
        return title


def get_books(dataset_language, searched_author):
    books_finding = dataset_language[
        dataset_language.author.str.contains(
            searched_author.lower(), case=False, na=True, flags=re.IGNORECASE,
            regex=False)]
    books_finding = books_finding.groupby("title").count().sort_values(
        "id", ascending=False).reset_index()
    return books_finding.title


def get_description(box, book_title):
    if box:
        st.markdown("#### Book description:")
        book_description(book_title)


def book_description(title):
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


def get_rec(corr_dataset, best_box, worst_box):
    best_corr = corr_dataset.book.head(NUMBER_OF_RECOMMENDATIONS)
    worst_corr = corr_dataset.book.tail(NUMBER_OF_RECOMMENDATIONS)

    if len(corr_dataset) <= NUMBER_OF_RECOMMENDATIONS:
        if best_box or worst_box:
            st.markdown("#### This book doesn't have enough data!")
    else:
        if best_box:
            st.markdown("#### Best recommendations:")
            rec_images(best_corr)

        if worst_box:
            st.markdown("#### Worst recommendations:")
            rec_images(worst_corr)


def rec_images(book_corr):
    cols = st.columns(3)
    for i in range(3):
        if i == 0:
            check_list = [0, 3, 6]
        elif i == 1:
            check_list = [1, 4, 7]
        else:
            check_list = [2, 5, 8]

        for index, value in enumerate(book_corr):
            if index in check_list:
                df_corr = get_corr_df(value)
                cols[i].image(get_corr_img(df_corr), width=170)
                cols[i].write(f"<b>{df_corr.title}</b>", unsafe_allow_html=True)
                cols[i].write(f"by {df_corr.author}")


def get_corr_df(title):
    book_corr_data = get_book_frame(dataset, title)
    return book_corr_data


def get_book_frame(data_base, book_name):
    url_img = data_base[data_base.title.str.lower() == book_name].iloc[0]
    return url_img


def get_corr_img(df_corr):
    return Image.open(requests.get(df_corr.image, stream=True).raw)


def get_book_column(title, column):
    book_data = dataset[dataset.title == title]
    return book_data[column].iloc[0]


def get_rating(title):
    book_data = dataset_lowercase[dataset_lowercase.title == title]
    book_rating = book_data.groupby("title").mean()
    return book_rating.rating.mean()


def publisher_languages():
    """
    Language dict where value is first number in ISBN.
    """
    return {"English": ["0", "1"], "French": "2", "German": "3"}


def get_language(selected_language):
    """
    Function returns  dataset with selected language.
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





