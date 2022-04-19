import pandas as pd
from pandas import DataFrame

RATING_AMOUNTS = 8
NUMBER_OF_RECOMMENDATIONS = 10
BOOKS_PATH = "csv_files/BX-Books.csv"
RATING_PATH = "csv_files/BX-Book-Ratings.csv"


def load_csv(path: str):
    """
    Load dataset from csv to pandas.
    """
    return pd.read_csv(path, encoding="cp1251", sep=";",
                       on_bad_lines="skip", low_memory=False)


def load_data(path: str):
    """
    Loads the dataset and makes adjustments.
    """
    data = load_csv(path)
    if path == RATING_PATH:
        data = data[data["Book-Rating"] != 0]
        # only books with multiple user ratings
        data = data[data.groupby('ISBN')['ISBN'].transform('size') >= RATING_AMOUNTS]
    return data


def merged_dataset(ratings_base: DataFrame, books_base: DataFrame):
    """
    Merged rename dataset without unused columns.
    """
    # merge datasets
    df = pd.merge(ratings_base, books_base, on=["ISBN"])

    # only needed columns
    df = df[["User-ID", "ISBN", "Book-Rating", "Book-Title", "Book-Author", "Image-URL-M"]]

    # rename columns
    df = df.rename(columns={
        "User-ID": "id", "ISBN": "isbn", "Book-Rating": "rating",
        "Book-Title": "title", "Book-Author": "author", "Image-URL-M": "image"
    })
    return df


def lowercase_dataset(merged_data: DataFrame):
    """
    Converts whole dataset to lowercase.
    """
    return merged_data.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)


books = load_data(BOOKS_PATH)
ratings = load_data(RATING_PATH)
dataset = merged_dataset(books, ratings)
dataset_lowercase = lowercase_dataset(dataset)
