import os
import boto3
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)
S3_BUCKET = os.getenv('S3_BUCKET')
SETTINGS_FILE_KEY = "configuration/settings.json"
s3 = session.client('s3')

output_path = os.getenv('OUTPUT_PATH', './tmp')
camera_name = os.getenv('CAMERA_NAME', f'CAMERA_{uuid.uuid4().hex[:8]}')



def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def upload_files(folder):
    '''Recursively uploads files in the given folder to S3 bucket'''

    # TODO - implement error handling (i.e., network failures, etc.)

    for item in os.listdir(folder):
        item_full_path = f'{folder}/{item}'

        if os.path.isdir(item_full_path):
            upload_files(item_full_path)
        if os.path.isfile(item_full_path):
            print(f'Uploading clip {item_full_path}')
            date, start_time, motion_flag = item_full_path.lstrip(output_path)[:-4].split('_')
            year, month, day = date.split('-')

            upload_object_folder = 'footage/activity' if motion_flag == "CONTAINS-MOTION" else 'footage/normal'

            upload_key = f'{upload_object_folder}/{year}-{month}/{day}/{start_time}_{camera_name}.mp4'

            s3.upload_file(item_full_path, S3_BUCKET, upload_key, ExtraArgs={'ContentType': "video/mp4"})
            
            print(f'done uploading clip {upload_key}')
            # Delete the file locally
            os.remove(item_full_path)

def get_and_parse_settings_file():
    '''Get the settings file from the s3 bucket.'''

    s3.download_file(S3_BUCKET, SETTINGS_FILE_KEY, 'settings.json')

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    return settings
