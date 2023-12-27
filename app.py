from flask import Flask, request, jsonify
import json
from sqlalchemy import create_engine, MetaData, Table
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.build_corpus import init_api, concatenate_row_values
from modules.search import search, load_corpus, load_vect, get_document_id


app = Flask(__name__)

data = init_api()
corpus = load_corpus()
vectorizers = load_vect()
tables = ["articles", "food", "questions", "recipes"]


# # Définition de l'endpoint de recherche v2
@app.route("/search", methods=["GET"])
def search_api():
    query = request.args.get("query", "")
    table_choices = request.args.get("table", tables)

    if not query:
        return jsonify({"error": "Aucune requête fournie."}), 400

    try:
        table_choices = table_choices.split(
            ","
        )  # Sépare les noms de tables si plusieurs sont fournis
        all_scores = []
        for table_choice in table_choices:
            if table_choice in tables:
                table_results = search(query, data, corpus, vectorizers, table_choice)
                for score, row in table_results:
                    doc_id = get_document_id(row)
                    all_scores.append((score, row, table_choice, doc_id))
        all_scores = sorted(all_scores, key=lambda x: x[0], reverse=True)[:10]

        formatted_results = [
            {
                "score": score,
                "document_id": doc_id,
                "document": concatenate_row_values(row),
                "table": table,
            }
            for score, row, table, doc_id in all_scores
        ]

        return jsonify(
            {"query": query, "table": table_choices, "results": formatted_results}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
