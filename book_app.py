import streamlit as st
import book_rec as br
import re
import description_scraper as ds
import requests
from PIL import Image


def main():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.image('book_logo.png', width=300)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users", value=f"""{br.number_of_users}""")
    col2.metric(label="Number of Books", value=f"""{br.number_of_books}""")
    col3.metric(label="Number of Ratings", value=f"""{br.number_of_ratings}""")

    user_name = st.text_input("Enter your name:")

    if user_name:
        select_genres = st.multiselect("Select your favorite genres:", br.genres)
        if select_genres:

            book_author = st.selectbox(f"Select your favorite author:", br.select_authors)

            if book_author:
                books_finding = br.books_relevant['Book-Title'][
                    br.books_relevant['Book-Author'].str.contains(book_author.lower(), case=False, na=True,
                                                                  flags=re.IGNORECASE, regex=False)]
                books_list = br.get_data(books_finding.to_frame(), 'Book-Title')

                book_name = st.selectbox(f'Select your favorite book from {book_author}', books_list)
                check1, check2, check3 = st.columns(3)
                description_box = check1.checkbox("Book description", value=False)
                best_box = check2.checkbox("Best recommendations", value=False)
                worst_box = check3.checkbox("Worst recommendations", value=False)
                result = br.main(br.dataset_lowercase, book_name.lower(), book_author.lower(),
                                 [book_name.lower()])

                if description_box:
                    st.markdown('#### Book description:')
                    book_description(book_name, book_author)

                if best_box:
                    st.markdown('#### Best recommendations:')
                    for i in result[0][0]['book']:
                        book_data = br.get_dataset_for_corr(br.dataset_base, i)
                        book_description(book_data['Book-Title'], book_data['Book-Author'])

                if worst_box:
                    st.markdown('#### Worst recommendations:')
                    idx = 0
                    book_list_corr = result[0][0]['book'].to_list()

                    for i in range(len(book_list_corr) - 1):
                        cols = st.columns(3)

                        if idx < len(book_list_corr) - 1:
                            book_corr_data = br.get_dataset_for_corr(br.dataset_base, book_list_corr[i])
                            book_corr_name = book_corr_data['Book-Title']
                            book_corr_author = book_corr_data['Book-Author']
                            url_img = br.get_book_img(br.dataset_base, book_corr_name)
                            book_cover = Image.open(requests.get(url_img, stream=True).raw)
                            cols[0].image(book_cover, width=170,
                                          caption=f'{book_corr_name} by {book_corr_author}')
                        idx += 1

                        if idx < len(book_list_corr) - 1:
                            cols[1].image(images_of_related_books[idx], width=175,
                                          caption=f'{names_of_related_books[idx]} by {authors_of_related_books[idx]}')
                        idx += 1
                        if idx < len(book_list_corr) - 1:
                            cols[2].image(images_of_related_books[idx], width=175,
                                          caption=f'{names_of_related_books[idx]} by {authors_of_related_books[idx]}')
                            idx = idx + 1
                        else:
                            break


                    cols = st.columns(3)
                    if
                    for i in range(2)
                    for i in result[0][0]['book']:
                        book_data = br.get_dataset_for_corr(br.dataset_base, i)
                        book_description(book_data['Book-Title'], book_data['Book-Author'])


def books_short_desc(book_name, book_author):
    url_img = br.get_book_img(br.dataset_base, book_name)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    col1, col2, col3 = st.columns(3)
    col1.image(book_cover, width=170)
    col2.write(f"<b>{book_name}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{book_author}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{round(br.get_book_rating(br.dataset_base, book_name), 1)}/10</b>", unsafe_allow_html=True)
    soup_for_book = ds.get_soup_book(book_name)
    col2.write(ds.get_description(soup_for_book))


def book_description(book_name, book_author):
    url_img = br.get_book_img(br.dataset_base, book_name)
    book_cover = Image.open(requests.get(url_img, stream=True).raw)
    col1, col2 = st.columns((1, 2.5))
    col1.image(book_cover, width=170)
    col2.write(f"<b>{book_name}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{book_author}</b>", unsafe_allow_html=True)
    col2.write(f"<b>{round(br.get_book_rating(br.dataset_base, book_name), 1)}/10</b>", unsafe_allow_html=True)
    soup_for_book = ds.get_soup_book(book_name)
    col2.write(ds.get_description(soup_for_book))


if __name__ == '__main__':
    main()
