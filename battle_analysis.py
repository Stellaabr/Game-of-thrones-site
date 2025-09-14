import pandas as pd
import numpy as np



def choice(slider_value, df):
    if slider_value == '298':
        return df.query('year == 298').to_dict('records')
    elif slider_value == '299':
        return df.query('year == 299').to_dict('records')
    else:  # 300
        return df.query('year == 300').to_dict('records')




def battle_outcome_by_king(df):
    kings = np.unique(np.concatenate([
        df['attacker_king'].dropna().values,
        df['defender_king'].dropna().values
    ]))

    results = {}
    for king in kings:
        attacker_mask = (df['attacker_king'] == king)
        defender_mask = (df['defender_king'] == king)

        attacker_wins = np.mean(df.loc[attacker_mask, 'attacker_outcome'] == 'win')
        defender_losses = np.mean(df.loc[defender_mask, 'attacker_outcome'] == 'win')

        results[king] = {
            'Attacker Win Rate': attacker_wins,
            'Defender Loss Rate': defender_losses,
            'Total Battles': np.sum(attacker_mask) + np.sum(defender_mask)
        }

    return pd.DataFrame(results).T




def analyze_battle_data_numpy(df):
    attacker_kings = df["attacker_king"].values
    defender_kings = df["defender_king"].values

    def get_king_stats(kings_array):
        kings, counts = np.unique(kings_array[~pd.isna(kings_array)], return_counts=True)
        top_idx = np.argsort(-counts)[:5]
        return list(zip(kings[top_idx], counts[top_idx]))  # Возвращаем список кортежей

    return {
        'attackers': get_king_stats(attacker_kings),
        'defenders': get_king_stats(defender_kings)
    }










def get_army_stats(sizes_array, kings_array, king_name):
    mask = ~np.isnan(sizes_array) & (kings_array == king_name)
    return np.mean(sizes_array[mask]) if np.any(mask) else 0




