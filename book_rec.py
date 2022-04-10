# import
import pandas as pd
import numpy as np

# load ratings
ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating'] != 0]

# load books
books = pd.read_csv('BX-Books.csv',  encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)

def main(book_name, book_author):
    #users_ratigs = pd.merge(ratings, users, on=['User-ID'])
    dataset = pd.merge(ratings, books, on=['ISBN'])
    dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

    #book_name = "the fellowship of the ring (the lord of the rings, part 1)"
    #book_author = "tolkien"


    book_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == book_name) & (dataset_lowercase['Book-Author'].str.contains(book_author))]
    book_readers = book_readers.tolist()
    book_readers = np.unique(book_readers)

    # final dataset
    books_of_author_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(book_readers))]

    # Number of ratings per other books in dataset
    number_of_rating_per_book = books_of_author_readers.groupby(['Book-Title']).agg('count').reset_index()

    #select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
    books_to_compare = books_to_compare.tolist()

    ratings_data_raw = books_of_author_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_author_readers['Book-Title'].isin(books_to_compare)]

    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

    # reset index to see User-ID in every row
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')


    result_list = []
    worst_list = []

    #Take out the book from correlation dataframe
    dataset_corr_without_your_book = dataset_for_corr.copy(deep=False)
    if book_name in dataset_corr_without_your_book:
        dataset_corr_without_your_book.drop(book_name, axis=1, inplace=True)

    # empty lists
    book_titles = []
    correlations = []
    avgrating = []

    # corr computation
    for book_title in list(dataset_corr_without_your_book.columns.values):
        book_titles.append(book_title)
        correlations.append(dataset_for_corr[book_name].corr(dataset_corr_without_your_book[book_title]))
        tab=(ratings_data_raw[ratings_data_raw['Book-Title'] == book_title].groupby(ratings_data_raw['Book-Title']).mean())
        avgrating.append(tab['Book-Rating'].min())
    # final dataframe of all correlation of each book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)), columns=['book', 'corr', 'avg_rating'])
    corr_fellowship.head()

    # top 10 books with highest corr
    result_list.append(corr_fellowship.sort_values('corr', ascending = False).head(10))

    #worst 10 books
    worst_list.append(corr_fellowship.sort_values('corr', ascending = False).tail(10))

    #print("Correlation for book:", Books_list[0])
    #print("Average rating of LOR:", ratings_data_raw[ratings_data_raw['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1'].groupby(ratings_data_raw['Book-Title']).mean()))
    #rslt = result_list[0]
    #print(rslt)
    return result_list