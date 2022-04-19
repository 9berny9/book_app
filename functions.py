
def publisher_languages():
    languages = {"English": ["0", "1"], "French": "2", "German": "3"}
    return languages


def get_language(data, selected_language):
    language_condition = publisher_languages()
    return data[data.isbn.str.startswith(tuple(language_condition[selected_language]), na=False)]


def get_genres():
    genres_list = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
                   "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
                   "Historical Fiction", "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery",
                   "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science",
                   "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel",
                   "Young Adult"]
    return genres_list


def get_dataset_for_corr(data_base, book_name):
    url_img = data_base[data_base.title.str.lower() == book_name].iloc[0]
    return url_img


def get_book_author(data, title):
    book_data = data[data.title == title]
    return book_data.author.iloc[0]


def get_book_img(data, title):
    book_data = data[data["Book-Title"] == title]
    return book_data["Image-URL-L"].iloc[0]


def get_book_rating(data_low, title):
    book_data = data_low[data_low["Book-Title"] == title]
    book_rating = book_data.groupby("Book-Title").mean()
    return book_rating["Book-Rating"].mean()
