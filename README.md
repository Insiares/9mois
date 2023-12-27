## Docker cmd 
### Pull image
```docker pull getmeili/meilisearch:v1.5```

### Run a container 
docker run -it --rm \
  -p 7700:7700 \
  -e MEILI_MASTER_KEY='MASTER_KEY'\
  -v $(pwd)/meili_data:/meili_data \
  getmeili/meilisearch:v1.5

# -- 
# test unitaire
# optimiser le tfidf - fuzzy search (flexibilité sur l'orthographe) - stop words - le vecteur all tables
# proposer une api d'update de l'index (ou autre route)
# merge le get de l'id documents
# ---