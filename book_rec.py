# import
import pandas as pd
from load_data import RATING_AMOUNTS, dataset_lowercase


def recommender(book_choice: str, book_author: str):
    author_readers = author_find(book_choice, book_author)

    #  final dataset with users, books and ratings
    books_of_author_readers = dataset_lowercase[(dataset_lowercase.id.isin(author_readers))]
    ratings_data_raw = ratings_data(books_of_author_readers)
    ratings_data_raw_nodup = ratings_nodup(ratings_data_raw)
    dataset_for_corr = ratings_data_raw_nodup.pivot(index='id', columns='title', values='rating')
    result_dataset = all_correlations(book_choice, dataset_for_corr, ratings_data_raw_nodup)
    return result_dataset


def author_find(book_name: str, book_author: str):
    """
    The function returns dataframe of users who have rated author.
    """
    author_readers = dataset_lowercase.id[(dataset_lowercase.title == book_name) & (
        dataset_lowercase.author.str.contains(book_author))]
    return dataset_lowercase[(dataset_lowercase.id.isin(author_readers.unique()))]


def ratings_data(books_of_author_readers):
    # Number of ratings per other books in dataset
    number_of_rating_per_book = books_of_author_readers.groupby(['title']).agg('count').reset_index()
    # select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book.title[number_of_rating_per_book.id >= RATING_AMOUNTS]
    books_to_compare = books_to_compare.tolist()
    # create dataset
    ratings_data_raw = books_of_author_readers[['User-ID', 'Book-Rating', 'Book-Title']][
        books_of_author_readers['Book-Title'].isin(books_to_compare)]
    return ratings_data_raw


def ratings_nodup(ratings_data_raw):
    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(['id', 'title']).rating.mean()
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

    # pridavat pouze do jednoho listu

    # corr computation
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        correlations.append(dataset_for_corr[book].corr(dataset_of_other_books[book_title]))
        tab = (ratings_data_raw[ratings_data_raw.title == book_title].groupby(
            ratings_data_raw.title).mean())
        avgrating.append(tab.rating.min())
    # final dataframe of all correlation for book

    # prejmenovat fellowship protoze
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])
    return corr_fellowship


