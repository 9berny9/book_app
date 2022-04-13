import book_rec as bc

dataset_base = bc.dataset_merge()
dataset_lowercase = bc.lowercase(dataset_base)


def unique_list(dataset_base):
    df = dataset_base['Book-Author'].sort_values().dropna()
    df = list(df.unique())
    df.insert(0, '')
    return df


df_authors = unique_list(dataset_base)

genres = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
          "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
          "Historical Fiction",
          "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy",
          "Poetry",
          "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality",
          "Sports",
          "Thriller", "Travel", "Young Adult"]
