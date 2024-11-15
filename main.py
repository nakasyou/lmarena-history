import pandas as pd
import bar_chart_race as bcr
import numpy as np
import glob
import pickle
from tqdm import tqdm

elo_results = {}
for csv_path in tqdm(glob.glob('./chatbot-arena-leaderboard/elo_results_*.pkl')):
    date = csv_path[40:-4]
    with open(csv_path, 'rb') as f:
        elo_results[date] = pickle.load(f)

elo_scores = {}
for date, elo in elo_results.items():
    scores = None
    if 'elo_rating_online' in elo:
        scores = elo['elo_rating_online']
    elif 'full' in elo:
        scores = elo['full']['elo_rating_online']
    elif 'text' in elo:
        scores = elo['text']['full']['elo_rating_final'].to_dict()
    else:
        raise TypeError(elo.keys())

    elo_scores[date] = scores

all_models = set()
for scores in elo_scores.values():
    for model in scores.keys():
        all_models.add(model)
df_source = {}
for date, values in elo_scores.items():
    df_source[date] = {key: values.get(key, 0) for key in all_models}
df = pd.DataFrame.from_dict(df_source, orient='index').sort_index()
