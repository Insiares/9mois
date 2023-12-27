import json
from sqlalchemy import create_engine, MetaData, Table
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib 
import os
import numpy as np
from modules.db import process_table, connect_db
import nltk

def load_stop_words(path):
    with open(path, "r") as file:
        return json.load(file)
    
def init_api():
    engine, metadata = connect_db()
    stop_words = load_stop_words("stop_words_french.json") #TODO : clarify path
    tables = ['articles', 'food', 'questions', 'recipes']
    data = {table: process_table(engine, metadata, table) for table in tables}
    # Préparation du vectorisateur TF-IDF

    vectorizers = {table: TfidfVectorizer(stop_words=stop_words, max_df=0.9) for table in tables}

    for table in tables:
        docs = data[table]
        vectorizers[table].fit_transform(docs)

    #Save the vectorizers

    save_files_path = './ML/'
    for key, vect in vectorizers.items():
        save_path = os.path.join(save_files_path, str(key+'.sav'))
        joblib.dump(vect, save_path)

    #build corpus and export it
    corpus = {table : vectorizers[table].transform(data[table]) for table in tables}

    for key, mat in corpus.items():
        save_path = os.path.join('./data/', str(key))
        np.save(save_path, mat)
    
    return data