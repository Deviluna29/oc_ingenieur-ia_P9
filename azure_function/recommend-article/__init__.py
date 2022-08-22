import logging
import os
from math import *
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
    blob_articles = BlobClient.from_connection_string(conn_str=connect_str, container_name="incontainer", blob_name='articles_embeddings.pickle')
    blob_clicks = BlobClient.from_connection_string(conn_str=connect_str, container_name="incontainer", blob_name='all_clicks.pickle')

    dl_articles = blob_articles.download_blob().readall()
    dl_clicks = blob_clicks.download_blob().readall()

    # Load to pickle
    articles_pkl = pickle.loads(dl_articles)
    articles_df = pd.DataFrame(articles_pkl, columns=["embedding_" + str(i) for i in range(articles_pkl.shape[1])])

    clicks_pkl = pickle.loads(dl_clicks)
    clicks_df = pd.DataFrame(clicks_pkl)

except Exception as ex:
    print('Exception:')
    print(ex)

# Recommandation Content-Based
def contentBasedRecommendArticle(articles, clicks, user_id, n=5):

    articles_read = clicks[clicks['user_id'] == user_id]['click_article_id'].tolist()

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.params.get('id')
    if not id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')

    if id:

        recommended = contentBasedRecommendArticle(articles_df, clicks_df, id)

        return func.HttpResponse(str(recommended))

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass an id in the query string or in the request body for a personalized response.",
             status_code=200
        )
