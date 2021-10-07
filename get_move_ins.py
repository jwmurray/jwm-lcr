#!/usr/bin/env python3

import json
from lcr import API as LCR

import json
from lcr import API as LCR
import pandas as pd
from sqlalchemy import create_engine
import pymysql


username = "gardenway"
password = "lancer83"
unit_number = 259950
lcr = LCR(username, password, unit_number)

months = 5
move_ins = lcr.members_moved_in(months)

df = pd.DataFrame.from_dict(move_ins)

cnx = create_engine('mysql+pymysql://user:pass@localhost/test')   

# create table from DataFrame
df.to_sql('test', cnx, if_exists='replace', index = False)

# query table
df = pd.read_sql('SELECT * FROM test', cnx)
df.head()

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='pass',
                             db='test')
cursor = connection.cursor()

# Create table
cols = df.columns
table_name = 'test'
ddl = ""
for col in cols:
    ddl += "`{}` text,".format(col)

sql_create = "CREATE TABLE IF NOT EXISTS `{}` ({}) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;".format(table_name, ddl[:-1])
cursor.execute(sql_create)

for member in move_ins:
    # print("{},\t\taddr: {}, \t\tMoved in on {}".format(member['name'], member['address'], member['moveDate']))
    print(member)