import pandas as pd
import boto3
from io import StringIO
from config import BUCKET_NAME, FILE_KEY

def load_data_from_s3():
    s3 = boto3.client('s3')
    csv_obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    body = csv_obj['Body'].read().decode('utf-8')
    return pd.read_csv(StringIO(body))
