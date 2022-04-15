import streamlit as st
import book_rec as br
import re
import prices_scraper as ps

st.write("""
# bookREC
Find friends for your book!
""")

user_name = st.text_input("Enter your name:")
if user_name:
    st.write(f'Your name is: {user_name}')
    select_genres = st.multiselect("Select your favorite genres:", br.genres)
    if select_genres:

        book_author = st.selectbox(f"Select your favorite author:", br.select_authors)

        if book_author:
            st.write(f'You selected: {book_author}')
            books_finding = br.books_relevant['Book-Title'][br.books_relevant['Book-Author'].str.contains(book_author.lower(), case=False, na=True, flags=re.IGNORECASE, regex=False)]
            books_list = br.get_data(books_finding.to_frame(), 'Book-Title')

            book_name = st.selectbox(f'Select your favorite book from {book_author}', books_list)
            st.write(f'You selected: {book_name} and users rating is: {"book_rating"}')

            if st.button("Get description"):
                st.write(ps.book_desc)

            if st.button("Get recommendations"):
                result = br.main(br.dataset_lowercase, book_name.lower(), book_author.lower(), [book_name.lower()])
                for index, row in result.iterrows():
                    st.write(row['book'], row['corr'], row['avg_rating'])
