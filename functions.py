import book_rec as bc
import pandas as pd


def unique_list(data):
    relevant_data = data.groupby('Book-Author').count()
    relevant_data = relevant_data.sort_values("Book-Author").reset_index()
    relevant_data = relevant_data.to_list()
    relevant_data.insert(0, '')
    return relevant_data

def relevant_books(data):
    ratings_relevant = data.groupby(['ISBN']).count()
    ratings_relevant = ratings_relevant.reset_index()
    ratings_relevant = ratings_relevant['ISBN'][ratings_relevant['User-ID'] > 70]
    ratings_relevant = data[data['ISBN'].isin(ratings_relevant)]
    return ratings_relevant

def get_data(data, column):
    relevant_data = data.groupby([column]).count()
    relevant_data = relevant_data.sort_values(by=column).reset_index()
    relevant_data = relevant_data[column].to_list()
    relevant_data.insert(0, '')
    return relevant_data

dataset_base = bc.dataset_merge()
dataset_lowercase = bc.lowercase(dataset_base)
books_relevant = relevant_books(dataset_base)
author_list = get_data(books_relevant, 'Book-Author')


genres = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
          "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
          "Historical Fiction",
          "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy",
          "Poetry",
          "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality",
          "Sports",
          "Thriller", "Travel", "Young Adult"]
