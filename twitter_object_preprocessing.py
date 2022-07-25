## Preprocessing twitter defined object to be used in the model
import pandas as pd
import numpy as np
from typing import TypeVar, List, Dict, Tuple, Union, Any


PandasDataFrame = TypeVar("pandas.core.frame.DataFrame")


class Object:
    def __init__(
        self, base_data: PandasDataFrame
    ) -> None:
        self.base_data = base_data
        self.base_data = base_data
        self.columns_to_process = base_data.columns.tolist()
        self.columns_processed = []
        self.tables = {}

    def get_processed_columns(self) -> List[str]:
        return self.columns_processed

    def get_tables_name_created(self) -> List[str]:
        return list(self.tables.keys())

    def expand_dict_column(
        self, column: str, keys: List[str], data: PandasDataFrame
    ) -> PandasDataFrame:
        """
        expand a dict column to a list of columns

        Args:
            column (str): Column name to expand
            key (List[str]): list of keys in the dict to get from the dict
            data (PandasDataFrame): Dataframe to expand

        Returns:
            PandasDataFrame: Dataframe with the expanded column
        """
        data.dropna(subset=[column], inplace=True)
        for key in keys:
            data[key] = data[column].apply(lambda x: x.get(key, np.nan))
        return data


class TweetObject(Object):
    def __init__(
        self, base_data: PandasDataFrame
    ) -> None:
        super().__init__(base_data)
        self.columns_in_tweet_table = ['id', 'created_at', 'text', 'author_id',
                                       'possibly_sensitive', 'conversation_id',
                                       'source', 'reply_settings', 'retweet_count',
                                       'like_count', 'quote_count', 'reply_count',
                                       'tweet_type', 'lang']

    def base_table_creation(self):
        processed_columns = list(
            set(self.columns_in_tweet_table).intersection(self.columns_to_process)
        )
        self.columns_processed.extend(processed_columns)

        self.base_data['tweet_type'] = 0

        self.base_data['tweet_type']+= self.base_data['id'].isin(
            self.tables['quoted_tweet_mapping']['tweet_id'])
        
        self.base_data['tweet_type']+= 2 * self.base_data['id'].isin(
            self.tables['retweeted_tweet_mapping']['tweet_id'])
        
        self.base_data['tweet_type'] += 3 * self.base_data['id'].isin(
            self.tables['replied_to_tweet_mapping']['tweet_id'])   

        self.tables['tweet_data'] = self.base_data[self.columns_in_tweet_table]     

        return self.columns_in_tweet_table

    def public_metric_column_processing(self):
        """
        Preprocess the public metric columns
        Expands the public metric columns to a list of columns
        """

        default_columns_defined_in_tweet_object = [
            "retweet_count",
            "reply_count",
            "like_count",
            "quote_count",
        ]

        self.expand_dict_column(
            "public_metrics", default_columns_defined_in_tweet_object, self.base_data
        )

        self.columns_in_tweet_table.extend(default_columns_defined_in_tweet_object)
        self.columns_processed.append("public_metrics")

    def referenced_tweets_processing(self):
        """
        Process the referenced tweets column.
        Creates Mapping tables for quote, retweets, and replies.
        retweet_data, reply_data, quote_data
        """

        columns_needed = ["id", "in_reply_to_user_id", "referenced_tweets"]

        data = self.base_data[columns_needed]
        data = data.explode("referenced_tweets")
        data = data.dropna(subset=["referenced_tweets"])

        data.rename(columns={"id": "tweet_id"}, inplace=True)

        self.expand_dict_column("referenced_tweets", ["id", "type"], data)

        data.rename(
            columns={"id": "referenced_tweet_id", "type": "tweet_type"}, inplace=True
        )

        columns_for_each = {
            "quoted": ["tweet_id", "referenced_tweet_id"],
            "retweeted": ["tweet_id", "referenced_tweet_id"],
            "replied_to": [
                "tweet_id",
                "referenced_tweet_id",
                "in_reply_to_user_id",
            ],
        }

        for key, value in columns_for_each.items():
            table_name = key + "_tweet_mapping"
            self.tables[table_name] = data[data["tweet_type"] == key]
            self.tables[table_name] = self.tables[table_name][value]

        self.columns_processed.append("referenced_tweets")
    
    def processing(self):
        
        self.public_metric_column_processing()
        self.referenced_tweets_processing()
        self.base_table_creation()


# class Entities(Object):

#     def __init__(self, base_data: PandasDataFrame, columns_to_process: List[str]) -> None:
#         super().__init__(base_data, columns_to_process)

#     def urls_processing(self, ):
#         return url