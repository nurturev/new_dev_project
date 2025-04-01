import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

BUCKET_NAME = "nv-tenant-dataset-models"
FILE_KEY = "202/pdl_raw_company_info/pdl_raw_company_info_1732559219.335818.csv"
