# import
import pandas as pd
import numpy as np


def dataset_merge(books_base, ratings_base):
    dataset = pd.merge(ratings_base, books_base, on=['ISBN'])
    return dataset


def isbn_languages():
    languages = {"English": ["0", "1"], "French": "2", "German": "3", "Japan": "4", "Czech": "80",
                 "Spain": "84", "Others" : "All"}
    return languages


def lowercase(data):
    """
    Function
    :return:
    """
    return data.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)


def main(dataset_low, book_choice, book_author):
    author_readers = author_find(dataset_low, book_choice, book_author)
    # final dataset with users, books and ratings
    books_of_author_readers = dataset_low[(dataset_low['User-ID'].isin(author_readers))]
    ratings_data_raw = ratings_data(books_of_author_readers)
    ratings_data_raw_nodup = ratings_nodup(ratings_data_raw)
    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
    result_dataset = all_correlations(book_choice, dataset_for_corr, ratings_data_raw_nodup)
    return result_dataset


def author_find(dataset_low, book_name, book_author):
    """
    The function returns array list of users who have rated author.
    """

    author_readers = dataset_low['User-ID'][(dataset_low['Book-Title'] == book_name) & (
        dataset_low['Book-Author'].str.contains(book_author))]
    author_readers = author_readers.tolist()
    author_readers = np.unique(author_readers)
    return author_readers


def ratings_data(books_of_author_readers):
    # Number of ratings per other books in dataset
    number_of_rating_per_book = books_of_author_readers.groupby(['Book-Title']).agg('count').reset_index()
    # select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
    books_to_compare = books_to_compare.tolist()
    # create dataset
    ratings_data_raw = books_of_author_readers[['User-ID', 'Book-Rating', 'Book-Title']][
        books_of_author_readers['Book-Title'].isin(books_to_compare)]
    return ratings_data_raw


def ratings_nodup(ratings_data_raw):
    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
    # reset index to see User-ID in every row
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
    return ratings_data_raw_nodup


def all_correlations(book_choice, dataset_for_corr, ratings_data_raw_nodup):
    result_list = []

    # Take out the author's selected book from correlation dataframe
    dataset_of_other_books = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop(book_choice, axis=1, inplace=True)

    corr_fellowship = correlation_by_book(dataset_of_other_books, dataset_for_corr, book_choice, ratings_data_raw_nodup)

    # all corr books
    result_list.append(corr_fellowship.sort_values('corr', ascending=False))
    return result_list


def correlation_by_book(dataset_of_other_books, dataset_for_corr, book, ratings_data_raw):
    # empty lists
    book_titles = []
    correlations = []
    avgrating = []
    # corr computation
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        correlations.append(dataset_for_corr[book].corr(dataset_of_other_books[book_title]))
        tab = (ratings_data_raw[ratings_data_raw['Book-Title'] == book_title].groupby(
            ratings_data_raw['Book-Title']).mean())
        avgrating.append(tab['Book-Rating'].min())
    # final dataframe of all correlation for book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])
    return corr_fellowship


def relevant_books(data):
    ratings_relevant = data.groupby(['ISBN']).count().reset_index()
    ratings_relevant = ratings_relevant['ISBN'][ratings_relevant['User-ID'] > 70]
    ratings_relevant = data[data['ISBN'].isin(ratings_relevant)]
    return ratings_relevant


def get_book_rating(data_low, title):
    book_data = data_low[data_low['Book-Title'] == title]
    book_rating = book_data.groupby('Book-Title').mean()
    return book_rating['Book-Rating'].mean()


def get_book_img(data, title):
    book_data = data[data['Book-Title'] == title]
    return book_data['Image-URL-L'].iloc[0]


def get_data(data, column):
    relevant_data = data.groupby([column]).count()
    relevant_data = relevant_data.sort_values(by=column).reset_index()
    relevant_data = relevant_data[column].to_list()
    relevant_data.insert(0, '')
    return relevant_data


def get_best_value(data, column, column2, avg):
    data_values = data.groupby([column]).count().reset_index()
    if avg == 'sum':
        value = data_values[column2].sum()
    elif avg == 'mean':
        value = data_values[column2].mean()
    else:
        value = data_values[column2].count()
    return value


def get_genres():
    genres_list = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
                   "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
                   "Historical Fiction", "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery",
                   "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science",
                   "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel",
                   "Young Adult"]
    return genres_list


def get_dataset_for_corr(data_base, book_name):
    url_img = data_base[data_base['Book-Title'].str.lower() == book_name].iloc[0]
    return url_img


# ---------------RUN--------------------------
# load data
books = pd.read_csv('csv_files/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
ratings = pd.read_csv('csv_files/BX-Book-Ratings.csv', encoding='cp1251', sep=';', on_bad_lines='skip',
                      low_memory=False)
ratings = ratings[ratings['Book-Rating'] != 0]
# ratings merge with books
dataset_base = dataset_merge(books, ratings)
# dataset with only lowercase
dataset_lowercase = lowercase(dataset_base)
# aggregations for app
number_of_users = get_best_value(dataset_base, 'User-ID', 'User-ID', 'count')
number_of_books = get_best_value(dataset_base, 'ISBN', 'Book-Title', 'count')
number_of_ratings = get_best_value(dataset_base, 'User-ID', 'ISBN', 'sum')
# list with all books genres
genres = get_genres()
# books with a lot of ratings
books_relevant = relevant_books(dataset_base)
# list with relevant authors for searching
select_authors = get_data(books_relevant, 'Book-Author')
languages = isbn_languages()
