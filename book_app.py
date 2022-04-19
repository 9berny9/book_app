import streamlit as st
import requests
import re
import scraper
import functions as f
from PIL import Image
from book_rec import recommender
from load_data import books, ratings, dataset, dataset_lowercase,\
    NUMBER_OF_RECOMMENDATIONS


# prejmenovat
def run_app():
    read_style()
    header()
    user_name = st.text_input("Enter your name:")

    # dat do funkce
    if user_name:
        select_genres = st.multiselect("Select your favorite genres:",
                                       f.get_genres())
        if select_genres:
            publisher_language = st.selectbox("Select publisher's language:",
                                              f.publisher_languages().keys())
            if publisher_language:
                book_author = st.text_input("Select author's last name:")
                books_language = f.get_language(dataset, publisher_language)

                if book_author:
                    book_title = st.selectbox(f"Select book's name:",
                                              get_books(books_language,
                                                        book_author))
                    check1, check2, check3 = st.columns(3)
                    description_box = check1.checkbox("Book description",
                                                      value=False)
                    best_box = check2.checkbox("Best recommendations",
                                               value=False)
                    worst_box = check3.checkbox("Worst recommendations",
                                                value=False)
                    # volat jenom jednou br main do promenne
                    if not recommender(book_title.lower(), book_author.lower()):
                        if description_box:
                            st.markdown("#### Book description:")
                            book_description(book_title)
                        if best_box:
                            st.markdown("#### This book doesn't have enough data!")
                        if worst_box:
                            st.markdown("#### This book doesn't have enough data!")
                    else:
                        result = recommender(book_title.lower(), book_author.lower())
                        if description_box:
                            st.markdown("#### Book description:")
                            book_description(book_title)

                        if best_box:
                            st.markdown("#### Best recommendations:")
                            # dat do konstanty 10
                            book_list_corr = result[0]["book"].head(NUMBER_OF_RECOMMENDATIONS).to_list()
                            recommendation(book_list_corr)

                        if worst_box:
                            st.markdown("#### Worst recommendations:")
                            book_list_corr = result[0]["book"].tail(NUMBER_OF_RECOMMENDATIONS).to_list()
                            recommendation(book_list_corr)


def read_style():
    with open("style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def header():
    st.image("book_logo.png", width=300)
    # create three columns abreast
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users",
                value=f"{len(ratings.groupby('User-ID'))}")
    col2.metric(label="Number of Books",
                value=f"{len(books['ISBN'])}")
    col3.metric(label="Number of Ratings",
                value=f"{len(ratings['Book-Rating'])}")


def book_rec_img(book_corr, column, column_number, number):
    book_corr_data = f.get_dataset_for_corr(dataset, book_corr[column_number])
    book_corr_name = book_corr_data.title
    book_corr_author = book_corr_data.author
    url_img = f.get_book_img(dataset, book_corr_name)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    column[number].image(book_cover, width=170,
                         caption=f"{book_corr_name} by {book_corr_author}")


def recommendation(book_corr):
    # a pouzit enumerate misto indexu
    idx = 0
    for i in range(len(book_corr) - 1):
        cols = st.columns(3)

        # pouzit pouze jeden if a hodit do for cyklu
        if idx < len(book_corr) - 1:
            book_rec_img(book_corr, cols, idx, 0)
        idx += 1

        if idx < len(book_corr) - 1:
            book_rec_img(book_corr, cols, idx, 1)
        idx += 1
        if idx < len(book_corr) - 1:
            book_rec_img(book_corr, cols, idx, 2)
            idx = idx + 1
        else:
            break


def book_description(title):
    url_img = f.get_book_img(dataset, title)
    author = f.get_book_author(dataset, title)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    col1, col2 = st.columns((1, 2.5))
    col1.image(book_cover, width=170)
    col2.write(f"<b>{title}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{author}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{round(f.get_book_rating(dataset_lowercase, title.lower()), 1)}/10</b>", unsafe_allow_html=True)
    soup_for_book = scraper.get_soup_book(title)
    col2.write(scraper.get_description(soup_for_book))


@st.cache(allow_output_mutation=True)
def get_books(dataset_language, searched_author):
    books_finding = dataset_language[
        dataset_language.author.str.contains(
            searched_author.lower(), case=False, na=True, flags=re.IGNORECASE,
            regex=False)]
    books_finding = books_finding.groupby("title").count().\
        sort_values("id", ascending=False).reset_index()
    return books_finding.title


# dat do zvlast souboru na spusteni

if __name__ == "__main__":
    run_app()
