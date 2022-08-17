import os

import pandas as pd

# Concatène tous les fichiers clicks dans un unique Dataframe
def get_all_clicks_files(path):
    clicks_df = pd.DataFrame()
    for file in os.listdir(path):
        df = pd.read_csv(path + file)
        clicks_df = pd.concat([clicks_df, df], axis=0)

    return clicks_df