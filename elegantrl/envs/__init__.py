import os
import numpy as np
import pandas as pd
from pathlib import Path

def load_data_from_disk(tech_id_list=None):
    path = Path(__file__).parent
    df_pwd = os.path.abspath(str(path) + '/China_A_shares.pandas.dataframe')
    npz_pwd = os.path.abspath(str(path) + '/China_A_shares.numpy.npz')
    tech_id_list = [
        "macd", "boll_ub", "boll_lb", "rsi_30", "cci_30", "dx_30", "close_30_sma", "close_60_sma",
    ] if tech_id_list is None else tech_id_list

    if os.path.exists(npz_pwd):
        ary_dict = np.load(npz_pwd, allow_pickle=True)
        close_ary = ary_dict['close_ary']
        tech_ary = ary_dict['tech_ary']
    elif os.path.exists(df_pwd):  # convert pandas.DataFrame to numpy.array
        df = pd.read_pickle(df_pwd)

        tech_ary = []
        close_ary = []
        df_len = len(df.index.unique())  # df_len = max_step
        for day in range(df_len):
            item = df.loc[day]

            tech_items = [item[tech].values.tolist() for tech in tech_id_list]
            tech_items_flatten = sum(tech_items, [])
            tech_ary.append(tech_items_flatten)

            close_ary.append(item.close)

        close_ary = np.array(close_ary)
        tech_ary = np.array(tech_ary)

        np.savez_compressed(npz_pwd, close_ary=close_ary, tech_ary=tech_ary, )
    else:
        error_str = f"| StockTradingEnv need {df_pwd} or {npz_pwd}" \
                    f"\n  download the following files and save in `.`" \
                    f"\n  https://github.com/Yonv1943/Python/blob/master/scow/China_A_shares.numpy.npz" \
                    f"\n  https://github.com/Yonv1943/Python/blob/master/scow/China_A_shares.pandas.dataframe"
        raise FileNotFoundError(error_str)
    return close_ary, tech_ary
