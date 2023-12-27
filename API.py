from flask import Flask, request, jsonify
import json
from sqlalchemy import create_engine, MetaData, Table
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Fonction pour charger la liste des stop words
def load_stop_words(path):
    with open(path, "r") as file:
        return json.load(file)

# Fonction pour concaténer les valeurs textuelles de toutes les colonnes
def concatenate_row_values(row):
    return ' '.join(str(value) for value in row if isinstance(value, str))

# Fonction pour traiter une table
def process_table(engine, metadata, table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        result_set = connection.execute(table.select()).fetchall()
    concatenated_docs = [concatenate_row_values(row) for row in result_set]
    return concatenated_docs, result_set

# Initialisation de la connexion à la base de données et du metadata
engine = create_engine("mysql+pymysql://root:root@localhost:3306/9mois")
metadata = MetaData()

# Chargement des stop words
stop_words = load_stop_words("stop_words_french.json")

# Traitement des tables et consolidation des données
tables = ['articles', 'food', 'questions', 'recipes']
data = {table: process_table(engine, metadata, table) for table in tables}

# Préparation du vectorisateur TF-IDF
vectorizers = {table: TfidfVectorizer(stop_words=stop_words) for table in tables}
for table in tables:
    docs, _ = data[table]
    vectorizers[table].fit_transform(docs)

# Fonction de recherche
def search(query, table_name):
    if table_name != "Toutes":
        documents, _ = data[table_name]
        vectorizer = vectorizers[table_name]
        tfidf_matrix = vectorizer.transform(documents)
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        ranked_scores = sorted([(score, doc) for doc, score in zip(documents, scores)], reverse=True)
        return ranked_scores[:10]  # 10 meilleurs résultats
    else:
        all_scores = []
        for table in tables:
            documents, _ = data[table]
            vectorizer = vectorizers[table]
            tfidf_matrix = vectorizer.transform(documents)
            query_vec = vectorizer.transform([query])
            scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
            all_scores.extend([(score, doc, table) for doc, score in zip(documents, scores)])
        return sorted(all_scores, key=lambda x: x[0], reverse=True)[:10]

# Définition de l'endpoint de recherche
@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    table_choice = request.args.get('table', 'Toutes')

    if not query:
        return jsonify({'error': 'Aucune requête fournie.'}), 400

    try:
        results = search(query, table_choice)
        formatted_results = [
            {'score': score, 'document': doc, 'table': table if table_choice == 'Toutes' else table_choice}
            for score, doc, table in results
        ] if table_choice == 'Toutes' else [{'score': score, 'document': doc} for score, doc in results]
        return jsonify({
            'query': query,
            'table': table_choice,
            'results': formatted_results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    


