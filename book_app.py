import streamlit as st
import book_rec as br
import re

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def main():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.image('logo.png', width=300)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users", value=f"""{br.number_of_users}""")
    col2.metric(label="Number of Books", value=f"""{br.number_of_books}""")
    col3.metric(label="Number of Ratings", value=f"""{br.number_of_ratings}""")

    user_name = st.text_input("Enter your name:")

    if user_name:
        st.write(f'Your name is: {user_name}')
        select_genres = st.multiselect("Select your favorite genres:", br.genres)
        if select_genres:

            book_author = st.selectbox(f"Select your favorite author:", br.select_authors)

            if book_author:
                st.write(f'You selected: {book_author}')
                books_finding = br.books_relevant['Book-Title'][
                    br.books_relevant['Book-Author'].str.contains(book_author.lower(), case=False, na=True,
                                                                  flags=re.IGNORECASE, regex=False)]
                books_list = br.get_data(books_finding.to_frame(), 'Book-Title')

                book_name = st.selectbox(f'Select your favorite book from {book_author}', books_list)
                if book_name:
                    st.write(f'{book_name} rating is: {round(br.get_book_rating(br.dataset_base, book_name), 1)}')

                    if st.button("Get recommendations"):
                        result = br.main(br.dataset_lowercase, book_name.lower(), book_author.lower(),
                                         [book_name.lower()])
                        best_books = result[0][0]
                        worst_books = result[1][0]
                        print(best_books)
                        print(worst_books)
                        box1, box2, box3 = st.columns(3)
                        box1.radio('b','c')
                        box2.radio('a','d')
                        box3.radio('v','g')



if __name__ == '__main__':
    main()
