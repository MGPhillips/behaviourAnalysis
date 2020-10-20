import pandas as pd

def load_pickle_to_pandas(path):

    return pd.read_pickle(path)

def save_pd_to_pickle(df, savepath):

    return df.to_pickle(savepath)


