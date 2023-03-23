import os
import boto3
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

S3_BUCKET = os.getenv('S3_BUCKET')
output_path = os.getenv('OUTPUT_PATH', './tmp')
completed_video_output_path = f'{output_path}/completed/'

SYSTEM_SETTINGS_FILE_KEY = 'configuration/settings.json'
LOCAL_CONFIG_FOLDER = 'config'
LOCAL_SYSTEM_SETTINGS_FILE = f'{LOCAL_CONFIG_FOLDER}/settings.json'
CAMERA_IDENTIFER_FILE = f'{LOCAL_CONFIG_FOLDER}/CAMERA_IDENTIFIER.txt'


session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)
s3 = session.client('s3')


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def upload_videos(folder, camera_id):
    '''Recursively uploads videos in the given folder to the S3 bucket. Inserts the camera id in each new object key.'''
    # TODO - implement error handling (i.e., network failures, etc.)

    for item in os.listdir(folder):
        item_full_path = f'{folder}/{item}'

        if os.path.isdir(item_full_path):
            upload_videos(item_full_path, camera_id)
        if os.path.isfile(item_full_path):
            date, start_time, motion_flag = item_full_path.split(f'{folder}/')[1][:-4].split('_')

            year, month, day = date.split('-')

            upload_object_folder = 'footage/activity' if motion_flag == "CONTAINS-MOTION" else 'footage/normal'

            upload_key = f'{upload_object_folder}/{year}-{month}/{day}/{start_time}_{camera_id}.mp4'

            s3.upload_file(item_full_path, S3_BUCKET, upload_key, ExtraArgs={'ContentType': "video/mp4"})
            
            # Delete the file locally
            os.remove(item_full_path)


def get_and_parse_settings_files(camera_id):
    '''Get the system settings and camera settings files from the s3 bucket. Returns a dictionary representing the settings.'''

    s3.download_file(S3_BUCKET, SYSTEM_SETTINGS_FILE_KEY, LOCAL_SYSTEM_SETTINGS_FILE)

    with open(LOCAL_SYSTEM_SETTINGS_FILE) as settings_file:
        settings = json.load(settings_file)

    try:
        camera_config_file = f'configuration/clients/{camera_id}.json'
        local_camera_config_file = f'{LOCAL_CONFIG_FOLDER}/{camera_id}.json'
        s3.download_file(S3_BUCKET, camera_config_file, local_camera_config_file)

        
        with open(local_camera_config_file) as camera_config_file:
            camera_config = json.load(camera_config_file)

            settings['camera'] = camera_config
    except:
        pass

    return settings


def get_camera_id():
    '''Gets the camera id from the config file. Generates one if it does not exist.'''

    if os.path.exists(CAMERA_IDENTIFER_FILE):
        with open(CAMERA_IDENTIFER_FILE) as f:
            id = f.readlines()[0]
    else:
        with open(CAMERA_IDENTIFER_FILE, 'w') as f: 
            id = uuid.uuid4().hex[:8]
            f.write(id)

    return id

