
from typing import List
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
ratings = pd.read_csv("C:\\Users\\JaredPeck\\Documents\\reccomendation_system\\app\\csv\\ratings.csv")
books = pd.read_csv("C:\\Users\\JaredPeck\\Documents\\reccomendation_system\\app\\csv\\books.csv")
import re

def clean_title(title):
    return re.sub(r"\s*\(.*?\)", "", title)
pd.set_option('display.max_columns', None)


combined_df = books.merge(ratings,  on = "book_id")

cleaned_df =  combined_df[["book_id", 'original_publication_year', "title",   'authors', 'language_code', 'average_rating',
                     'ratings_count', 'work_ratings_count', 'work_text_reviews_count','user_id', 'rating', "image_url"]]
cleaned_df 

cleaned_df.shape

x = cleaned_df["user_id"].value_counts() > 100
y= x[x].index

ratings_with_books = cleaned_df[cleaned_df['user_id'].isin(y)]
ratings_with_books


number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()

number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)


final_rating = ratings_with_books.merge(number_rating, on='title')
final_rating["title"].apply(lambda x: clean_title(x))
final_rating["title"].value_counts()

final_rating = final_rating[final_rating['num_of_rating'] >= 50]

final_rating.drop_duplicates(['user_id','title'],inplace=True)


# pivot the table using the title as the Index, user_id as a column and the values as the rating
book_pivot = final_rating.pivot_table(columns='user_id', index='title', values= 'rating')


book_pivot = book_pivot.fillna(0)


# pass in the csr_matrix to make it computationally faster
from scipy.sparse import csr_matrix

# add pivot table to the sparse matrix 
book_sparse = csr_matrix(book_pivot)

book_pivot.to_csv("book_pivoted.csv")




def get_book_vectors(df: pd.DataFrame, book_titles: List[str]) -> np.ndarray:
    book_vectors = []
    for title in book_titles:
        if title in df.index:
            book_vectors.append(df.loc[title].values)
        else:
            raise ValueError(f"The book '{title}' is not in the DataFrame index.")
    return np.array(book_vectors)

def books_recommendation(user_liked_books: List[str], model: NearestNeighbors, df: pd.DataFrame, n_neighbors: int = 8) -> List[str]:
    book_vectors = get_book_vectors(df, user_liked_books)
    average_vector = np.mean(book_vectors, axis=0).reshape(1, -1)
    distance, suggestion = model.kneighbors(average_vector, n_neighbors=n_neighbors + len(user_liked_books))
    
    suggested_books = [df.index[suggestion[0][i]] for i in range(len(suggestion[0]))]
    
    filtered_suggestions = [book for book in suggested_books if book not in user_liked_books][:n_neighbors]
    
    return filtered_suggestions

user_liked_books = [
    'The Hunger Games (The Hunger Games, #1)',
    'Twilight (Twilight, #1)'
]

