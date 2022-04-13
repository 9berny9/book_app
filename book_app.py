import pandas as pd
import numpy as np
import streamlit as st
import book_rec


# load books
#books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
#books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', nrows=20)

genres = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
          "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
          "Historical Fiction",
          "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy",
          "Poetry",
          "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality",
          "Sports",
          "Thriller", "Travel", "Young Adult"]

st.write("""
# bookREC
Find friends for your book!
""")

user_name = st.text_input("Enter your name:")
if user_name:
    st.write(f'You selected: {user_name}')
    genres = st.multiselect("Select your favorite genres:", genres)
    if genres:
        book_author = st.text_input("What is your favorite author?")

        if book_author:
            st.write(f'You selected: {book_author}')
            books_data = book_rec.load_data(path='BX-Books.csv')
            books_finding = books_data[books_data['Book-Author'].str.contains(book_author, case=False, na=True)]

        #book_author = st.selectbox('Select your favorite book author', books_finding["Book-Author"])
        #st.write(f'You selected: {book_author}')


        #book_title = book_rec.books.loc[book_rec.books['Book-Author'] == book_author]['Book-Title']
            book_name = st.selectbox(f'Select your favorite book from {book_author}', books_finding['Book-Title'])
            st.write(f'You selected: {book_name}')
            book_name = book_name.lower()
            more_books = [book_name]
            book_author = book_author.lower()
            print(book_name)
            print(more_books)
            print(book_author)


            if st.button("Get recommendations"):
                result = book_rec.main(book_name, book_author, more_books)
                st.write(result)


