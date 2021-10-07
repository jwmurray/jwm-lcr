import json
from lcr import API as LCR
import pandas as pd


def get_members_df_from_lcr(lcr):

    ward = lcr.member_list()
    # recommend_status = lcr.recommend_status()

    df = pd.DataFrame.from_dict(ward)
    return df

def get_profile_from_lcr(lcr, member_id):

    profile = lcr.individual_profile(member_id)
    profile_list = [profile]
    df = pd.DataFrame.from_dict(profile_list)

    return df