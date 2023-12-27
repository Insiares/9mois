import json
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
import numpy as np
from modules.db import process_table, connect_db
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk import download

download("punkt")


# Fonction pour concaténer les valeurs textuelles de toutes les colonnes
def concatenate_row_values(row):
    return "".join(str(value) for value in row if isinstance(value, str))


def load_stop_words(path):
    with open(path, "r") as file:
        return json.load(file)


def tokenizer_stemmer(text):
    stemmer = SnowballStemmer("french")
    tokens = word_tokenize(text, language="french")
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return stemmed_tokens


def init_api():
    engine, metadata = connect_db()
    stop_words = load_stop_words("./data/stop_words_french.json")
    tables = ["articles", "food", "questions", "recipes"]
    data = {table: process_table(engine, metadata, table) for table in tables}
    # Préparation du vectorisateur TF-IDF

    vectorizers = {
        table: TfidfVectorizer(
            tokenizer=tokenizer_stemmer,
            stop_words=stop_words
            )
        for table in tables
    }

    for table in tables:
        docs = [concatenate_row_values(row) for row in data[table]]
        vectorizers[table].fit_transform(docs)

    # Save the vectorizers

    save_files_path = "./ML/"
    for key, vect in vectorizers.items():
        save_path = os.path.join(save_files_path, str(key + ".sav"))
        joblib.dump(vect, save_path)

    corpus = {}
    for table in tables:
        documents = data[table]
        vectorizer = vectorizers[table]
        corpus[table] = vectorizer.transform(
            [concatenate_row_values(row) for row in documents]
        )

    for key, mat in corpus.items():
        save_path = os.path.join("./data/", str(key))
        np.save(save_path, mat)

    return data
