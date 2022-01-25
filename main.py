import datetime

from config import *
import pandas as pd
from functools import reduce


def create_df(path, df_list):
    df_temp = pd.read_csv(path, sep=",", usecols=[0, 1, 3, 4])
    type_var = df_temp["type"][0]
    df_temp.index = pd.to_datetime(df_temp["time"].str[:-12])
    df_temp[f"{type_var}_value"] = df_temp["value"]
    df_temp = df_temp.drop(columns=["value", "type", "time"])
    logger.debug(
        f"Dataframe read from file {path} after def create_df\n"
        f"{df_temp.head().to_string()} "
    )
    df_list.append(df_temp)


def valuation_formula(index, p_sum_value, power_fcr_value, df):
    minP_p = df['P_n'].loc[str(index-datetime.timedelta(seconds=30)):str(index)].min()
    if power_fcr_value + minP_p - (abs(d1) * P_nom_KHAR5CHPP) <= p_sum_value <= (power_fcr_value + minP_p + (abs(d1) * P_nom_KHAR5CHPP)):
        return 1
    else:
        return 0


def main():
    df_list = []
    dir_list = list(input_dir.rglob(f"{look_for_mask}*"))
    logger.info(f"Founded {len(dir_list)} file/-s:\n{dir_list}")
    for item in dir_list:
        create_df(item, df_list)
    df = reduce(
        lambda left, right: pd.merge(
            left, right, on=["time", "generator_name"], how="outer"
        ),
        df_list,
    )
    df["delta_f"] = frequency_nom - df["frequency_value"]
    df.loc[abs(df["delta_f"]) < 0.02, "delta_f"] = 0
    df.loc[abs(df["delta_f"]) > 0.2, "delta_f"] = 0.2
    df["P_p"] = (0.2 * P_nom_KHAR5CHPP * 100) / (
        50 * df["statizm_value"] * 0.01
    )  # 0.01 for %
    df["P_n"] = -5 * df["P_p"] * df["delta_f"]
    df.loc[df["P_n"] == -0.0, "P_n"] = 0
    # if (
    #     (
    #         df["power_fcr_value"]
    #         + df["P_n"].loc[str(df.index - datetime.timedelta(seconds=30)): df.index].min()
    #         - abs(d1) * P_nom_KHAR5CHPP
    #     )
    #     <= df["p_sum_value"]
    #     <= (
    #         df["power_fcr_value"]
    #         + df["P_n"].loc[str(df.index - datetime.timedelta(seconds=30)): df.index].min()
    #         + abs(d1) * P_nom_KHAR5CHPP
    #     )
    # ):
    #     df["solution"] = 1
    # else:
    #     df["solution"] = 0
    df_new = df.iloc[0:50]
    df_new['solution'] = df_new.apply(lambda row: valuation_formula(row.name, row['p_sum_value'], row['power_fcr_value'], df), axis=1)  # part of df for test
    print(df_new.to_string())
    # df['solution'] = df.apply(lambda row: valuation_formula(row.name, row['p_sum_value'], row['power_fcr_value'], df), axis=1) # full df
    # print(df.head(10).to_string())


if __name__ == "__main__":
    main()
