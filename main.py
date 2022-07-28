import  pandas as pd
import numpy as np
import os
from twitter_object_preprocessing import *

def insert_data_into_database(files: List[str], folder_path: str) -> None:
    for i in range(len(files)):
        print(files[i])
        data = pd.read_json(folder_path + '\\' +
                            files[i], orient='records', lines=True, chunksize=50)
        j = 0
        for chunk in data:
            j += 1

            ## Get tweet_objects data from the chunk
            curr_data = [chunk['data'],
                        chunk['includes'].apply(lambda x: x['tweets'])]
            curr_data = pd.concat(curr_data, ignore_index=True)
            tweets_data = pd.DataFrame(curr_data.explode().to_list())

            ## Get user_objects data from the chunk
            curr_user_data = [chunk['includes'].apply(lambda x: x['users'])]
            user_data = pd.concat(curr_user_data, ignore_index=True)
            user_data = pd.DataFrame(user_data.explode().to_list())

            tweet_object = TweetObject(tweets_data)
            tweet_object.processing()

            user_object = User(user_data)
            user_object.processing()
            break
        break
    return tweet_object, user_object

def get_files_and_insert():
    base_folder = "D:\Misogynistic"
    curr_task = "Search"
    folder_path = base_folder + "\\" + curr_task
    files = os.listdir(folder_path)
    tweet_object,user_object = insert_data_into_database(files, folder_path)
    return tweet_object, user_object
