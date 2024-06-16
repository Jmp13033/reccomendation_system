
import sys
from typing import List
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
ratings = pd.read_csv("C:\\Users\\JaredPeck\\Documents\\reccomendation_system\\app\\csv\\ratings.csv")
books = pd.read_csv("C:\\Users\\JaredPeck\\Documents\\reccomendation_system\\app\\csv\\books.csv")
final_ratings = pd.read_csv("C:\\Users\\JaredPeck\\Documents\\reccomendation_system\\app\\csv\\final_rating_df.csv")
import re



def load_pivot():
    global final_ratings
    final_ratings = final_ratings.drop("Unnamed: 0", axis= 1)
    book_pivot = final_ratings.pivot_table(columns='user_id', index='title', values= 'rating')
    book_pivot = book_pivot.fillna(0)
    
    return book_pivot
    


def clean_book_titles(book_list):
    cleaned_books = []
    for book in book_list:
        match = re.match(r'^(.*?)\s\((.*?),\s#\d+\)$', book)
        if match:
            title = match.group(1).strip()
            series = match.group(2).strip()
            if title.lower() != series.lower():
                cleaned_books.append(f"{series} {title}")
            else:
                cleaned_books.append(title)
        else:
            cleaned_books.append(book)
    return cleaned_books



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




