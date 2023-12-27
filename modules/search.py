import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

def load_vect():
    tables = ['articles', 'food', 'questions', 'recipes']
    base_path = './ML/'
    vect = { table : joblib.load(os.path.join(base_path, str(table+'.sav'))) for table in tables}
    return vect

def load_corpus():
    corpus = { 'articles' : np.load('./data/articles.npy', allow_pickle= True).item(),
               'food' : np.load('./data/food.npy', allow_pickle= True).item(),
                'questions' : np.load('./data/questions.npy', allow_pickle= True).item(),
                 'recipes' : np.load('./data/recipes.npy', allow_pickle= True).item() }
    return corpus

# Fonction de recherche
def search(query, data, corpus, vectorizers, table_name = 'Toutes'):
    tables = ['articles', 'food', 'questions', 'recipes']
    # corpus = load_corpus()
    # vectorizers = load_vect()
    # TODO : get it out of the loop
    if table_name != "Toutes":
        documents = data[table_name]
        vectorizer = vectorizers[table_name]
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, corpus[table_name]).flatten()
        ranked_scores = sorted([(score, doc) for doc, score in zip(documents, scores)], reverse=True)
        return ranked_scores[:10]  # 10 meilleurs résultats
    else:
        all_scores = []
        for table in tables:
            documents = data[table]
            vectorizer = vectorizers[table]
            query_vec = vectorizer.transform([query])
            scores = cosine_similarity(query_vec, corpus[table]).flatten()
            all_scores.extend([(score, doc, table) for doc, score in zip(documents, scores)])
        return sorted(all_scores, key=lambda x: x[0], reverse=True)[:10]