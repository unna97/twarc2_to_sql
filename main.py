import pandas as pd
import numpy as np
import os
from twitter_object_preprocessing import *
from sqlalchemy.dialects.postgresql import insert
import sqlalchemy as sa


def create_engine():

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'misogynistic_twitter',
            'USER': 'postgres',
            'PASSWORD': 'unnati',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        database_name=DATABASES['default']['NAME'],
    )

    engine = sa.create_engine(database_url, pool_pre_ping=True)
    return engine



def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_conflict_do_nothing()
    conn.execute(on_duplicate_key_stmt)



def insert_data_into_database(files: List[str], folder_path: str, engine) -> None:
    for i in range(len(files)):
        print(files[i])
        data = pd.read_json(
            folder_path + "\\" + files[i], orient="records", lines=True, chunksize=50
        )
        j = 0
        for chunk in data:
            j += 1

            ## Get tweet_objects data from the chunk
            curr_data = [chunk["data"], chunk["includes"].apply(lambda x: x["tweets"])]
            curr_data = pd.concat(curr_data, ignore_index=True)
            tweets_data = pd.DataFrame(curr_data.explode().to_list())

            ## Get user_objects data from the chunk
            curr_user_data = [chunk["includes"].apply(lambda x: x["users"])]
            user_data = pd.concat(curr_user_data, ignore_index=True)
            user_data = pd.DataFrame(user_data.explode().to_list())

            tweet_object = TweetObject(tweets_data)
            tweet_object.processing()
            ## Insert tweet_objects data into the database
            for cur_table in tweet_object.tables.keys():
                if len(tweet_object.tables[cur_table]) == 0:
                    print('Empty table: {}'.format(cur_table))
                else:
                    print('Table inserted: {}'.format(cur_table))
                    tweet_object.tables[cur_table].to_sql(
                        name=cur_table, con=engine, if_exists='append', index=False, method=insert_on_duplicate)

            user_object = User(user_data)
            user_object.processing()

            ## Insert user_objects data into the database
            for cur_table in user_object.tables.keys():
                if len(user_object.tables[cur_table]) == 0:
                    print('Empty table: {}'.format(cur_table))
                else:
                    print('Table inserted: {}'.format(cur_table))
                    user_object.tables[cur_table].to_sql(
                        name=cur_table, con=engine, if_exists='append', index=False, method=insert_on_duplicate)
    return tweet_object, user_object


def get_files_and_insert():
    base_folder = "D:\Misogynistic"
    curr_task = "Search"
    folder_path = base_folder + "\\" + curr_task
    files = os.listdir(folder_path)
    engine = create_engine()
    tweet_object, user_object = insert_data_into_database(files, folder_path, engine)
    return tweet_object, user_object
