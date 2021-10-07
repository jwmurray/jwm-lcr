#!/usr/bin/env python3

import argparse
import sys

import json
from tkinter import E
from lcr import API as LCR
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import ast
import datetime
from mysql_access import read_mysql_table_into_df, write_df_to_mysql_table, set_primary_key
from lcr_access import get_members_df_from_lcr, get_profile_from_lcr

mysql_user = "lcr_user"
mysql_password = "lcr_pass"
mysql_host = "localhost"
mysql_db = "lcr"
mysql_table = "members"
lcr_username = "gardenway"
lcr_password = "lancer83"
lcr_unit_number = 259950

def get_date_from_string_dict(string_dict):
    try:
        dict = ast.literal_eval(string_dict)
        date_str = dict['date']['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except:
        date = datetime.datetime.now()
    return date

def read_tables():
    df = read_mysql_table_into_df(mysql_user,mysql_password, mysql_host,mysql_db, mysql_table)

    df['birth_dt']=df['birth'].apply(get_date_from_string_dict) # .astype(datetime)

    write_df_to_mysql_table(df, mysql_user,mysql_password, mysql_host,mysql_db, 
        "members2")

    string_dict = "{'date': {'date': '2014-12-11', 'calc': '2014-12-11', 'display': '11 Dec 2014'}, 'monthDay': {'date': '0000-12-11', 'calc': '', 'display': '11 Dec'}, 'place': None, 'country': None}"


    
    df = get_members_df_from_lcr(username=username,
        password = password,
        unit_number=unit_number)

    newdate = get_date_from_string_dict(string_dict)

    
    # convert from string format to datetime format
    datetime = datetime.datetime.strptime(newdate, '%Y-%m-%d')



    # for member in move_ins:
    #     print("{}: {}".format(member, member['textAddress']))



    cnx = create_engine('mysql+pymysql://lcr_user:lcr_pass@localhost/lcr')   


    df = df.astype(str)
    # df[["nameFormats", "unitOrgsCombined", 
    #     "householdMember", "address", "birth", 
    #     "personStatusFlags"]] = df[["nameFormats", "unitOrgsCombined", 
    #     "householdMember", 
    #     "address", "birth", "personStatusFlags"]].astype(str)

    # df.drop('nameFormats', inplace=True, axis=1)
    # df.drop('unitOrgsCombined', inplace=True, axis=1)
    # df.drop('householdMember', inplace=True, axis=1)
    # df.drop('address', inplace=True, axis=1)
    # df.drop('birth', inplace=True, axis=1)
    # df.drop('personStatusFlags', inplace=True, axis=1)

    df[["age"]] = df[["age"]].astype(int)
    df[["legacyCmsId"]] = df[["legacyCmsId"]].astype(int)
    df[["member"]] = df[["member"]].astype(bool)
    df["birth"] = df.applymapget_date_from_string_dict(df["birth"])

    dict = ast.literal_eval(df.birth[1])
    date = get_date_from_string_dict(df.birth[1])

    # create table from DataFrame
    df.to_sql('lcr', cnx, if_exists='replace', index = False)

    for member in ward:
        jsonstr1 = json.dumps(member, indent=4)
        print(jsonstr1 )
        print ("")
        if member['email'] == 'john@gardenway.org':
            print("stop")

def read_from_lcr_and_save_to_sql(lcr):
    df = get_members_df_from_lcr(lcr)
    
    df = df.astype(str)

    df[["age"]] = df[["age"]].astype(int)
    # df[["member"]] = df[["member"]].astype(bool)
    df[["convert"]] = df[["convert"]].astype(bool)
    df[["unitNumber"]] = df[["unitNumber"]].astype(int)
    df[["legacyCmisId"]] = df[["legacyCmisId"]].astype(int)

    df['birth_dt']=df['birth'].apply(get_date_from_string_dict) # .astype(datetime)
    
    write_df_to_mysql_table(df, mysql_user,mysql_password, mysql_host,mysql_db, 
        "members")

    print(df.head())
    return lcr
    
def read_profile_from_lcr_and_save_to_sql(lcr, member_id, append="append"):
    df = get_profile_from_lcr(lcr, member_id)
    

    df = df.astype(str)
    df['member_id'] = member_id
    df['member_id'] = df['member_id'].astype(int)
    # df[["age"]] = df[["age"]].astype(int)
    # # df[["member"]] = df[["member"]].astype(bool)
    # df[["convert"]] = df[["convert"]].astype(bool)
    # df[["unitNumber"]] = df[["unitNumber"]].astype(int)

    # df['birth_dt']=df['birth'].apply(get_date_from_string_dict) # .astype(datetime)
    
    write_df_to_mysql_table(df, mysql_user,mysql_password, mysql_host,mysql_db, 
        "profiles")

    set_primary_key(mysql_user,mysql_password, 
        mysql_host,mysql_db, mysql_table)

    print(df.head())
    return lcr
    
def print_member(member):
    print(member)

def main():
    parser = argparse.ArgumentParser(description='Access member records from LCR.')
    parser.add_argument('--lcr', action='store_true')
    parser.add_argument('--members', '-m', action='store_true')
    parser.add_argument('--profile', action='store_true')
    args = parser.parse_args(["--members"])
    args = parser.parse_args(["--profile", "--lcr", "--members"])


    lcr = LCR(lcr_username, lcr_password, lcr_unit_number)

    if args.lcr:
        read_from_lcr_and_save_to_sql(lcr)
    
    if args.members:
        df = read_mysql_table_into_df(mysql_user,mysql_password, mysql_host,mysql_db, mysql_table)


        for index, row in df.iterrows():
            if index > 1:
                break
            print_member(row)
            # printprint(index, ': ', row['name'], 'has', row['calories'], 'calories.')

    if args.profile:
        # lcr = read_from_lcr_and_save_to_sql()
        profile = read_profile_from_lcr_and_save_to_sql(lcr, 3063752471)
        profile = read_profile_from_lcr_and_save_to_sql(lcr, 3063752471)
        profile = read_profile_from_lcr_and_save_to_sql(lcr, 5982079922)
        # profile = read_profile_from_lcr_and_save_to_sql(lcr, 29836363982)
        # request = lcr.individual_profile(3063752471)
        print(profile)

        

if __name__ == "__main__":
    main()

    