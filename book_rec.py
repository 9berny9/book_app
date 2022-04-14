# import
import pandas as pd
import numpy as np


def dataset_merge():
    books = pd.read_csv('BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
    ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
    ratings = ratings[ratings['Book-Rating'] != 0]

    #zkouska
    ratings = ratings.groupby(['ISBN']).count()
    ratings = ratings.reset_index()
    ratings = ratings['ISBN'][ratings['User-ID'] > 5]
    dataset = pd.merge(ratings, books, on=['ISBN'])
    return dataset


def lowercase(dataset_merge):
    """
    Function
    :return:
    """
    return dataset_merge.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)


def author_find(dataset_lowercase, book_name, book_author):
    """
    The function returns array list of users who have rated author.
    """

    author_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == book_name) & (
        dataset_lowercase['Book-Author'].str.contains(book_author))]
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

    # top_books = result_list[0][0]
    # worst_books = result_list[1][0]

    #book_rating = ratings_data_raw["Book-Rating"][ratings_data_raw['Book-Title'] == book_name].groupby(ratings_data_raw['Book-Title']).mean()
    return result_list
