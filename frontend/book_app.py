from frontend.functions import *
from backend.book_rec import recommender
from backend.load_data import books, ratings, NUMBER_OF_RECOMMENDATIONS


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
    with open("frontend/src/style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def header():
    st.image("frontend/src/book_logo.png", width=300)
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


def get_description(box, book_title):
    if box:
        st.markdown("#### Book description:")
        book_description(book_title)


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


