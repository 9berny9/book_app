# import
import pandas as pd
import numpy as np


def dataset_merge():
    books = pd.read_csv('csv_files/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
    ratings = pd.read_csv('csv_files/BX-Book-Ratings.csv', encoding='cp1251', sep=';', on_bad_lines='skip',
                          low_memory=False)
    ratings = ratings[ratings['Book-Rating'] != 0]
    dataset = pd.merge(ratings, books, on=['ISBN'])
    return dataset


def relevant_books(data):
    ratings_relevant = data.groupby(['ISBN']).count().reset_index()
    ratings_relevant = ratings_relevant['ISBN'][ratings_relevant['User-ID'] > 70]
    ratings_relevant = data[data['ISBN'].isin(ratings_relevant)]
    return ratings_relevant


def get_book_rating(data_low, title):
    book_data = data_low[data_low['Book-Title'] == title]
    book_rating = book_data.groupby('Book-Title').mean()
    return book_rating['Book-Rating'].mean()


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
                   "Historical Fiction",
                   "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal",
                   "Philosophy",
                   "Poetry",
                   "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense",
                   "Spirituality",
                   "Sports",
                   "Thriller", "Travel", "Young Adult"]
    return genres_list


def lowercase(data):
    """
    Function
    :return:
    """
    return data.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)


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


def all_correlations(books_choice, dataset_for_corr, ratings_data_raw_nodup):
    result_list = [[], []]

    for book in books_choice:
        # Take out the author's selected book from correlation dataframe
        dataset_of_other_books = dataset_for_corr.copy(deep=False)

        if book in dataset_for_corr:
            dataset_of_other_books.drop([book], axis=1, inplace=True)

        corr_fellowship = correlation_by_book(dataset_of_other_books, dataset_for_corr, book, ratings_data_raw_nodup)

        # top 10 books with highest corr
        result_list[0].append(corr_fellowship.sort_values('corr', ascending=False).head(8))
        # worst 10 books
        result_list[1].append(corr_fellowship.sort_values('corr', ascending=False).tail(8))
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
    # final dataframe of all correlation of each book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])
    return corr_fellowship


def main(dataset_lowercase, book_name, book_author, books_choice):
    author_readers = author_find(dataset_lowercase, book_name, book_author)
    # final dataset with users, books and ratings
    books_of_author_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(author_readers))]
    ratings_data_raw = ratings_data(books_of_author_readers)
    ratings_data_raw_nodup = ratings_nodup(ratings_data_raw)
    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')

    result_list = all_correlations(books_choice, dataset_for_corr, ratings_data_raw_nodup)

    return result_list


# RUN
dataset_base = dataset_merge()
dataset_lowercase = lowercase(dataset_base)
number_of_users = get_best_value(dataset_base, 'User-ID', 'User-ID', 'count')
number_of_books = get_best_value(dataset_base, 'ISBN', 'Book-Title', 'count')
number_of_ratings = get_best_value(dataset_base, 'User-ID', 'ISBN', 'sum')
genres = get_genres()
books_relevant = relevant_books(dataset_base)
select_authors = get_data(books_relevant, 'Book-Author')
