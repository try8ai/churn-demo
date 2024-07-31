from datetime import datetime, timedelta
import os

import pandas as pd

from superlinked.evaluation.charts.recency_plotter import RecencyPlotter
from superlinked.evaluation.vector_sampler import VectorSampler
from superlinked.framework.common.dag.context import CONTEXT_COMMON, CONTEXT_COMMON_NOW
from superlinked.framework.common.dag.period_time import PeriodTime
from superlinked.framework.common.embedding.number_embedding import Mode
from superlinked.framework.common.schema.schema import schema
from superlinked.framework.common.schema.schema_object import Integer
from superlinked.framework.common.schema.id_schema_object import IdField
from superlinked.framework.dsl.executor.in_memory.in_memory_executor import (
    InMemoryExecutor,
    InMemoryApp,
)
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.source.in_memory_source import InMemorySource
from superlinked.framework.dsl.space.text_similarity_space import TextSimilaritySpace
from superlinked.framework.dsl.space.number_space import NumberSpace
from superlinked.framework.dsl.space.recency_space import RecencySpace

LOGIN_DATASET_URL = "data/customer_logins_data.csv"

login_df: pd.DataFrame = pd.read_csv(LOGIN_DATASET_URL)
print(f"Accounts data dimensions: {login_df.shape}")
print(login_df.head())

print(login_df["churn_score"].head())

@schema
class LoginSchema:
    account_id: Integer
    user_id: IdField
    logins_month_1: Integer
    logins_month_2: Integer
    logins_month_3: Integer
    logins_month_4: Integer
    logins_month_5: Integer
    logins_month_6: Integer
    logins_month_7: Integer
    logins_month_8: Integer
    logins_month_9: Integer
    logins_month_10: Integer
    logins_month_11: Integer
    logins_month_12: Integer
    churn_score: Integer

