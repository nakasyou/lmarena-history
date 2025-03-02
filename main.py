import pandas as pd
import glob
import pickle
from tqdm import tqdm
import json

elo_results = {}
for csv_path in tqdm(glob.glob('./chatbot-arena-leaderboard/elo_results_*.pkl')):
    date = csv_path[40:-4]
    with open(csv_path, 'rb') as f:
        elo_results[date] = pickle.load(f)

TITLE_NORMALIZE = {
    'full': 'overall',
    'full_style_control': 'overall_style_control',
    'long': 'long_user'
}
def normalize_title(t: str) -> str:
    if t in TITLE_NORMALIZE:
        return TITLE_NORMALIZE[t]
    return t

scores_by_date = {}
for i, (date, elo) in enumerate(list(elo_results.items())[:]):
    scores = None
    if 'elo_rating_online' in elo:
        scores = {
            "text": {
                "overall": elo['elo_rating_online']
            }
        }
    elif 'text' in elo and 'vision' in elo:
        scores = {
            "text": {},
            "vision": {}
        }
        for title, rating in elo['text'].items():
            scores['text'][normalize_title(title)] = rating['elo_rating_final'].to_dict()
        for title, rating in elo['vision'].items():
            scores['vision'][normalize_title(title)] = rating['elo_rating_final'].to_dict()
    elif (
        ('dedup' in elo and 'english' in elo) or
        ('full' in elo and 'no_refusal' in elo and 'long_user' in elo) or
        ('full' in elo and 'chinese' in elo) or
        (len(elo.keys()) == 1 and 'full' in elo)
    ):
        scores = {
            'text': {}
        }
        for title, rating in elo.items():
            scores['text'][normalize_title(title)] = rating['elo_rating_final'].to_dict()

    else:
        raise TypeError(i, date, elo.keys())

    scores_by_date[date] = scores

with open('output/scores.json', 'w') as f:
    json.dump(scores_by_date, f, indent=2)
