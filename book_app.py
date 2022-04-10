import pandas as pd
import numpy as np
import streamlit as st


# load books
books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
#books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', nrows=20)

#genres = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
#          "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
#          "Historical Fiction",
#          "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy",
#          "Poetry",
#          "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality",
#          "Sports",
#          "Thriller", "Travel", "Young Adult"]

st.write("""
# bookREC
Find friends for your book!
""")

#user_name = st.text_input("Enter your name:")
#genres = st.multiselect("Select your favorite genres:", genres)
#find_book = st.text_input("Which author you finding?")
#books_finding = books['Book-Author'].str.contains(find_book)

book_author = st.selectbox('Select your favorite book author', books["Book-Author"])
st.write(f'You selected: {book_author}')

#book_author_last_name = book_author.split()[-1]
book_title = books.loc[books['Book-Author'] == book_author]['Book-Title']

if book_author:
    book_name = st.selectbox(f'Select your favorite book from {book_author}', book_title)


