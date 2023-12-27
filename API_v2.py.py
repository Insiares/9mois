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

# Fonction pour traiter une table
def process_table(engine, metadata, table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        result_set = connection.execute(table.select()).fetchall()
    return result_set

def concatenate_row_values(row):
    return ''.join(str(value) for value in row if isinstance(value, str))

# Initialisation de la connexion à la base de données et du metadata
engine = create_engine("mysql+pymysql://root:root@9mois.ownedge.fr:3306/9mois")
metadata = MetaData()

# Chargement des stop words
stop_words = load_stop_words("stop_words_french.json")

# Traitement des tables et consolidation des données
tables = ['articles', 'food', 'questions', 'recipes']
data = {table: process_table(engine, metadata, table) for table in tables}

# Préparation du vectorisateur TF-IDF
vectorizers = {table: TfidfVectorizer(stop_words=stop_words) for table in tables}
for table in tables:
    docs = [concatenate_row_values(row) for row in data[table]]
    vectorizers[table].fit_transform(docs)

# Fonction pour obtenir l'ID de la ligne en fonction de la table
def get_document_id(doc):
    return doc[0]

# Fonction de recherche
def search(query, table_name):
    if table_name != "Toutes":
        documents = data[table_name]
        vectorizer = vectorizers[table_name]
        tfidf_matrix = vectorizer.transform([concatenate_row_values(row) for row in documents])
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        ranked_scores = sorted([(score, row) for score, row in zip(scores, documents)], reverse=True, key=lambda x: x[0])
        return ranked_scores[:10]  # 10 meilleurs résultats
    else:
        all_scores = []
        for table in tables:
            documents = data[table]
            vectorizer = vectorizers[table]
            tfidf_matrix = vectorizer.transform([concatenate_row_values(row) for row in documents])
            query_vec = vectorizer.transform([query])
            scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
            all_scores.extend([(score, row, table) for score, row in zip(scores, documents)])
        return sorted(all_scores, key=lambda x: x[0], reverse=True)[:10]

# Définition de l'endpoint de recherche
@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    table_choices = request.args.get('table', 'Toutes')

    if not query:
        return jsonify({'error': 'Aucune requête fournie.'}), 400

    try:
        if table_choices != 'Toutes':
            table_choices = table_choices.split(',')  # Sépare les noms de tables si plusieurs sont fournis--
            all_scores = []
            for table_choice in table_choices:
                if table_choice in tables:
                    table_results = search(query, table_choice)
                    for score, row in table_results:
                        doc_id = get_document_id(row, table_choice)
                        all_scores.append((score, row, table_choice, doc_id))
            all_scores = sorted(all_scores, key=lambda x: x[0], reverse=True)[:10]
        else:
            all_scores = search(query, table_choices)
        

        formatted_results = [{
            'score': score,
            'document_id': doc_id,
            'document': concatenate_row_values(row),
            'table': table
        } for score, row, table, doc_id in all_scores]

        return jsonify({
            'query': query,
            'table': table_choices,
            'results': formatted_results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
