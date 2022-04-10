import pandas as pd
import numpy as np
import streamlit as st
import book_rec


# load books
#books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
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

book_author = st.selectbox('Select your favorite book author', book_rec.books["Book-Author"])
st.write(f'You selected: {book_author}')


book_title = book_rec.books.loc[book_rec.books['Book-Author'] == book_author]['Book-Title']

book_name = st.selectbox(f'Select your favorite book from {book_author}', book_title)
st.write(f'You selected: {book_name}')

if st.button("Get recommendations"):
    st.write(book_rec.main("the fellowship of the ring (the lord of the rings, part 1)", "tolkien"))



#book_rec.main(book_name, book_title)
