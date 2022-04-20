import pandas as pd
from pandas import DataFrame, Series
from backend.load_data import RATING_AMOUNTS, dataset_lowercase


def recommender(book_choice: str, book_author: str) -> DataFrame:
    """
    Main function returns correlation dataframe for the selected book.
    """
    author_readers = users_find(book_choice, book_author)
    # final dataset with users, books and ratings
    books_of_author_readers = dataset_lowercase[
        (dataset_lowercase.id.isin(author_readers))]
    ratings_data_raw = ratings_data(books_of_author_readers)
    dataset_for_corr = ratings_nodup(ratings_data_raw)
    result = book_correlations(dataset_for_corr, book_choice)
    return result


def users_find(book_name: str, book_author: str) -> Series:
    """
    The function returns dataframe of users who have rated author.
    """
    author_readers = dataset_lowercase.id[
        (dataset_lowercase.title == book_name) & (
            dataset_lowercase.author.str.contains(book_author))]
    author_readers = dataset_lowercase[
        (dataset_lowercase.id.isin(author_readers.unique()))].id
    return author_readers


def ratings_data(books_of_author_readers: DataFrame) -> DataFrame:
    """
    Function returns dataframe with the user's title rating.
    Only for higher number of ratings than threshold.
    """
    # Number of ratings per other books in dataset
    number_of_rating_per_book = books_of_author_readers.groupby(
        ['title']).count().reset_index()
    # select books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book.title[
        number_of_rating_per_book.id >= RATING_AMOUNTS].tolist()
    # create dataset without threshold
    ratings_data_raw = books_of_author_readers[['id', 'rating', 'title']][
        books_of_author_readers.title.isin(books_to_compare)]
    return ratings_data_raw


def ratings_nodup(ratings_data_raw: DataFrame) -> DataFrame:
    """
    Function returns dataframe where columns are titles, indexes are user id
    and values are ratings.
    """
    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(
        ['id', 'title']).rating.mean()
    # reset index to see User-ID in every row
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
    ratings_data_raw_nodup = ratings_data_raw_nodup.pivot(index='id',
                                                          columns='title',
                                                          values='rating')
    return ratings_data_raw_nodup


def book_correlations(dataset_for_corr: DataFrame, book: str) -> DataFrame:
    """
    Function returns dataframe for all correlations without selected book.
    Dataframe is sorted from the highest correlation.
    """
    recommended_books = []
    # corr computation
    for book_title in dataset_for_corr.columns.values:
        if book_title != book:
            corr = dataset_for_corr[book].corr(dataset_for_corr[book_title])
            avg_rating = dataset_for_corr[book_title].mean(skipna=True)
            recommended_books.append((book_title, corr, avg_rating))
    # final dataframe of all correlation for book
    correlations = pd.DataFrame(recommended_books,
                                columns=['book', 'corr', 'avg_rating'])
    result = correlations.sort_values('corr', ascending=False)
    return result
