# import
import pandas as pd
import numpy as np


def main(data_merge, book_choice, book_author):
    # dataset with only lowercase
    dataset_lowercase = data_merge.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)
    author_readers = author_find(dataset_lowercase, book_choice, book_author)

    if len(author_readers) > 10:
        #  final dataset with users, books and ratings
        books_of_author_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(author_readers))]
        ratings_data_raw = ratings_data(books_of_author_readers)
        ratings_data_raw_nodup = ratings_nodup(ratings_data_raw)
        dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
        result_dataset = all_correlations(book_choice, dataset_for_corr, ratings_data_raw_nodup)
        return result_dataset
    else:
        return False


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






