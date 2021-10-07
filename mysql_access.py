from mysqlx import IntegrityError, ProgrammingError
from sqlalchemy import create_engine, false
import pandas as pd


def read_mysql_table_into_df(mysql_user,mysql_password, mysql_host,mysql_db, mysql_table):
    db_connection_str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql(f"SELECT * FROM {mysql_table}", con=db_connection)
    return df

def set_primary_key(mysql_user,mysql_password, 
    mysql_host,mysql_db, mysql_table):
    db_connection_str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    db_connection = create_engine(db_connection_str)
    db_connection.execute('ALTER TABLE profiles ADD PRIMARY KEY (member_id);')


def write_df_to_mysql_table(df, mysql_user,mysql_password, 
    mysql_host,mysql_db, mysql_table, append = "replace"):
    db_connection_str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    db_connection = create_engine(db_connection_str)

# ALTER TABLE `lcr`.`profiles` 
# CHANGE COLUMN `member_id` `member_id` INT NOT NULL ,
# ADD PRIMARY KEY (`member_id`),
# ADD UNIQUE INDEX `member_id_UNIQUE` (`member_id` ASC) VISIBLE;
# ;

    try:
        df.to_sql(name = mysql_table, con=db_connection, if_exists=append, index = False)
    # except IntegrityError:
    #     df.to_sql(name = mysql_table, con=db_connection, if_exists='replace', index = False)
    # except ProgrammingError:
    #     df.to_sql(name = mysql_table, con=db_connection, if_exists='replace', index = False)
    except:
        df.to_sql(name = mysql_table, con=db_connection, if_exists='replace', index = False)


    return df