import logging
import os
from math import *
from heapq import nlargest
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import azure.functions as func
from azure.storage.blob import BlobClient,  __version__

try:
    logging.info("Azure Blob Storage v" + __version__)

    connect_str = os.getenv('AzureWebJobsStorage')

    ##### Chargement des fichiers #####
    # Download blobs
    blob_articles = BlobClient.from_connection_string(conn_str=connect_str, container_name="incontainer", blob_name='articles_embeddings.pickle')
    blob_users = BlobClient.from_connection_string(conn_str=connect_str, container_name="incontainer", blob_name='users.pickle')
    blob_model = BlobClient.from_connection_string(conn_str=connect_str, container_name="incontainer", blob_name='model_svd.pickle')

    # Load to pickle
    articles_df = pickle.loads(blob_articles.download_blob().readall())
    articles_df = pd.DataFrame(articles_df, columns=["embedding_" + str(i) for i in range(articles_df.shape[1])])

    users_df = pickle.loads(blob_users.download_blob().readall())

    model = pickle.loads(blob_model.download_blob().readall())

except Exception as ex:
    print('Exception:')
    print(ex)

# Recommandation Content-Based
def contentBasedRecommendArticle(articles, users, user_id, n=5):

    articles_read = users['click_article_id'].loc[user_id]

    if len(articles_read) == 0:
        return "L'utilisateur n'a lu aucun article"

    articles_read_embedding = articles.loc[articles_read]

    articles = articles.drop(articles_read)

    matrix = cosine_similarity(articles_read_embedding, articles)

    rec = []

    for i in range(n):
        coord_x = floor(np.argmax(matrix)/matrix.shape[1])
        coord_y = np.argmax(matrix)%matrix.shape[1]

        rec.append(int(coord_y))

        matrix[coord_x][coord_y] = 0
    
    rec.sort()

    return rec

# Recommandation Collaborative Filtering
def collaborativeFilteringRecommendArticle(articles, users, user_id, n=5):

    index = list(articles.index)

    articles_read = users['click_article_id'].loc[user_id]

    for ele in articles_read:
        if ele in index:
            index.remove(ele)

    results = dict()

    for i in index:
        pred = model['algo'].predict(user_id, i)
        results[pred.iid] = pred.est
    
    return nlargest(n, results, key = results.get)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        id = req_body.get('id')
        type = req_body.get('type')

    if id and type and isinstance(id, int) and isinstance(type, str):

        recommended = contentBasedRecommendArticle(articles_df, users_df, id) if type == "cb" else collaborativeFilteringRecommendArticle(articles_df, users_df, id)

        return func.HttpResponse(str(recommended), status_code=200)

    else:
        return func.HttpResponse(
             "Requête invalide.\nDans le body doit figurer sous format json :\n- id (int)\n- type (cb ou cf)",
             status_code=400
        )