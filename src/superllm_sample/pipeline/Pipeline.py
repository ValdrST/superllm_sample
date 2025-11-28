import json
import logging
from ..fetch.FetchPostHolder import FetchPostHolder
from ..models.Qwen import Qwen
from ..core.SQLResolver import SQLResolver
import pandas as pd
import time
from pangres import upsert

class Pipeline():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fetcher = FetchPostHolder()
        self.enricher = Qwen()
        sqlresolver = SQLResolver()
        self.engine = sqlresolver.get_engine('localhost')

    def fetch_source(self, limit = 100):
        logging.info('start fetch source')
        data = self.fetcher.fetch(limit = limit)
        logging.info('fetched {} records'.format(len(data)))
        return data

    def normalize(self, records):
        logging.info('start normalize')
        df = pd.json_normalize(records)
        expected = ['userId', 'id', 'title', 'body']
        for c in expected:
            if c not in df.columns:
                df[c] = None
        df = df[expected]
        return df
    
    def validate_df(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('start validate')
        issues = []
        invalid_id_mask = (
            df['id'].isna() |
            df['id'].astype(str).str.strip().isin(['', 'None', 'null'])
        )
        for i, row in df.iterrows():
            if pd.isna(row['id']) or not isinstance(row['id'], (int,)):
                issues.append((i, 'invalid_id', row['id']))
            if pd.isna(row['title']) or str(row['title']).strip()=='':
                issues.append((i, 'missing_title', row['id']))
        if issues:
            for issue in issues:
                logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{issue}")
            logging.warning('Validation found %d issues', len(issues))
        else:
            logging.info('No validation issues found')
        df = df[~invalid_id_mask].copy()
        return df

    def enrich_rows(self,df):
        logging.info('start enrich rows')
        df['llm_label'] = df.apply(lambda r: self.enricher.get_llm_label(r['title'], r['body']), axis=1)
        return df

    def persist_rows(self,df):
        logging.info('start persist')
        df.set_index(['id'],inplace = True,drop=True)
        try:
            upsert(con=self.engine,df=df,table_name='posts', if_row_exists='update',schema='public',create_table= False,add_new_columns=False)
        except:
            upsert(con=self.engine,df=df,table_name='posts', if_row_exists='update',schema='public',create_table= True,add_new_columns=True)
        logging.info('Persisted %d rows to posts table',len(df))

    def load_results(self, limit: int = 100):
        try:
            df = pd.read_sql('posts', con=self.engine)
        except Exception:
            return []
        if limit:
            return df.head(int(limit)).to_dict(orient='records')
        return df.to_dict(orient='records')
    

    def run_pipeline(self,limit: int = 100, enrich: bool = True):
        records = self.fetch_source(limit=limit)
        df = self.normalize(records)
        df = self.validate_df(df)
        df = self.enrich_rows(df)
        self.persist_rows(df)
        return df
            