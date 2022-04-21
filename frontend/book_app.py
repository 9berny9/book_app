from frontend.functions import *
from backend.book_rec import recommender
from backend.load_data import books, ratings, NUMBER_OF_RECOMMENDATIONS


def run_app():
    """
    Function creates streamlit app layouts.
    """
    read_style()
    header()
    genres = user_select()
    language = language_select(genres)
    df = language_dataframe(language)
    author = author_select(df)
    title = title_select(author, df)
    description_corr(title, author)


def read_style():
    """
    Function reads style.css for app.
    """
    with open("frontend/src/style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def header():
    """
    Function creates three columns with counting metrics.
    """
    st.image("frontend/src/book_logo.png", width=300)
    # create three columns abreast
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Number of Users",
                value=f"{len(ratings.groupby('User-ID'))}")
    col2.metric(label="Number of Books",
                value=f"{len(books['ISBN'])}")
    col3.metric(label="Number of Ratings",
                value=f"{len(ratings['Book-Rating'])}")


def user_select() -> list:
    """
    Function returns selected genres for user.
    """
    user_name = st.text_input("Enter your name:")
    if user_name:
        select_genres = st.multiselect("Select your favorite genres:",
                                       get_genres())
        return select_genres


def language_select(selected_genres: list) -> str:
    """
     Function returns selected publisher's language.
    """
    if selected_genres:
        publisher_language = st.selectbox("Select publisher's language:",
                                          publisher_languages().keys())
        return publisher_language


def language_dataframe(selected_language: str) -> DataFrame:
    """
    Function returns dataframe with publisher's books.
    """
    if selected_language:
        df_language = get_language(selected_language)
        return df_language


def author_select(df: DataFrame) -> str:
    """
    Function returns selected author from user.
    """
    if df is not None:
        author = st.text_input("Select author's last name:")
        return author


def title_select(selected_author: str, df: DataFrame) -> str:
    """
    Function returns selected book title
    """
    if selected_author:
        title = st.selectbox(f"Select book's name:",
                             get_books(df, selected_author))
        return title


def description_corr(title: str, author: str):
    """
    Function creates three checkboxes and reads dataframe recommendations.
    After selecting the box, it will create a description.
    """
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


def rec_images(book_corr):
    cols = st.columns(3)
    for i in range(3):
        if i == 0:
            check_list = [0, 3, 6]
        elif i == 1:
            check_list = [1, 4, 7]
        else:
            check_list = [2, 5, 8]

        for index, value in enumerate(book_corr):
            if index in check_list:
                df_corr = get_corr_df(value)
                cols[i].image(get_corr_img(df_corr), width=170)
                cols[i].write(f"""<p><b>{df_corr.title}</b></p> 
                                <p>{df_corr.author}</p>""",
                              unsafe_allow_html=True)