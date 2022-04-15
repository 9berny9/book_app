import streamlit as st
import book_rec as br
import re
import description_scraper as ds

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
                    st.markdown(f'''## {book_name} ''')
                    col1, col2 = st.columns(2)
                    col1.markdown(f'''### {book_author} ''')
                    col2.markdown(f'''#### {round(br.get_book_rating(br.dataset_base, book_name), 1)}/10''')
                    ## rating is: {round(br.get_book_rating(br.dataset_base, book_name), 1)}''')
                    st.write(f'''{ds.main(book_name)}''')
                    box1, box2 = st.columns(2)
                    result = br.main(br.dataset_lowercase, book_name.lower(), book_author.lower(),
                                     [book_name.lower()])
                    best = box1.button('Best recommendations')
                    worst = box2.button('Worst recommendations')
                    if best:
                        st.write(result[0][0])
                    elif worst:
                        st.write(result[1][0])






if __name__ == '__main__':
    main()
