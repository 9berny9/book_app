import book_rec as bc


def unique_list(data, column):
    relevant_data = data.groupby([column]).count()
    relevant_data = relevant_data.sort_values("User-ID").reset_index()
    relevant_data = relevant_data[column][relevant_data['User-ID'] > 20]
    relevant_data = relevant_data.to_list()
    relevant_data.insert(0, '')
    return relevant_data


relevant_data = ratings.groupby(['ISBN']).count()
relevant_data = relevant_data.reset_index()
relevant_data = relevant_data['ISBN'][relevant_data['User-ID'] > 5]
# ted mam knizky, ktere byly hodnoceny aspon 5x - > spojim je s knizkami vsemi
final = pd.merge(relevant_data, books, on=['ISBN'], how='inner')



dataset_base = bc.dataset_merge()
dataset_lowercase = bc.lowercase(dataset_base)
dataset_authors = unique_list(dataset_base, 'Book-Author')

genres = ["Art", "Business", "Chick-Lit", "Children's", "Christian", "Classics", "Comendy",
          "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Graphic Novels",
          "Historical Fiction",
          "History", "Horror", "LGBT", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy",
          "Poetry",
          "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality",
          "Sports",
          "Thriller", "Travel", "Young Adult"]
