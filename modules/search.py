import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
# from autocorrect import Speller


def load_vect():
    tables = ["articles", "food", "questions", "recipes"]
    base_path = "./ML/"
    vect = {
        table: joblib.load(os.path.join(base_path, str(table + ".sav")))
        for table in tables
    }
    return vect


def load_corpus():
    corpus = {
        "articles": np.load("./data/articles.npy", allow_pickle=True).item(),
        "food": np.load("./data/food.npy", allow_pickle=True).item(),
        "questions": np.load("./data/questions.npy", allow_pickle=True).item(),
        "recipes": np.load("./data/recipes.npy", allow_pickle=True).item(),
    }
    return corpus


def get_document_id(doc):
    return doc[0]


# Fonction de recherche
def search(query, data, corpus, vectorizers, table_name):
    documents = data[table_name]
    vectorizer = vectorizers[table_name]
    # spell = Speller('fr')
    # query_corr = spell(query)
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, corpus[table_name]).flatten()
    ranked_scores = sorted(
        [(score, row) for score, row in zip(scores, documents)],
        reverse=True,
        key=lambda x: x[0],
    )
    return ranked_scores[:10]  # 10 meilleurs résultats
