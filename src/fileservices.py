import os
import boto3
import asyncio
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)
S3_BUCKET = os.getenv('S3_BUCKET')
s3 = session.client('s3')

output_path = os.getenv('OUTPUT_PATH', './tmp')


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

async def upload_files(folder):
    sync_files_s3(folder)

def sync_files_s3(folder):
    '''Recursively uploads files in the given folder to S3 bucket'''

    # TODO - implement error handling (i.e., network failures, etc.)

    for item in os.listdir(folder):
        item_full_path = f'{folder}/{item}'

        if os.path.isdir(item_full_path):
            sync_files_s3(item_full_path)
        if os.path.isfile(item_full_path):
            upload_filename = item_full_path.lstrip(output_path)
            print(f'Uploading file {upload_filename}')
            s3.upload_file(item_full_path, S3_BUCKET, upload_filename)

            # Delete the file locally
            os.remove(item_full_path)

