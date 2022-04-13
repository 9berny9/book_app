import pandas as pd
import numpy as np
import streamlit as st
import book_rec
import functions as fnc
import re

st.write("""
# bookREC
Find friends for your book!
""")

user_name = st.text_input("Enter your name:")
if user_name:
    st.write(f'You selected: {user_name}')
    genres = st.multiselect("Select your favorite genres:", fnc.genres)
    if genres:
        #book_author = st.text_input("What is your favorite author?")
        book_author = st.selectbox(f"Select your favorite author:", fnc.df_authors)
        book_author_find = book_author.lower()

        if book_author:
            st.write(f'You selected: {book_author}')
            books_finding = fnc.dataset_base['Book-Title'][fnc.dataset_base['Book-Author']
                .str.contains(book_author_find, case=False, na=True, flags=re.IGNORECASE, regex=False)]
            books_finding = books_finding.sort_values().dropna()
            books_finding = list(books_finding.unique())

            # st.write(f'You selected: {book_author}')

            # book_title = book_rec.books.loc[book_rec.books['Book-Author'] == book_author]['Book-Title']
            book_name = st.selectbox(f'Select your favorite book from {book_author}', books_finding)
            st.write(f'You selected: {book_name}')
            book_name = book_name.lower()
            more_books = [book_name]
            book_author = book_author.lower()
            print(book_name)
            print(more_books)
            print(book_author)

            if st.button("Get recommendations"):
                result = book_rec.main(fnc.dataset_lowercase, book_name, book_author, more_books)
                st.write(result[0][0])
