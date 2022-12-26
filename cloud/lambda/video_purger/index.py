import boto3
import os
import json
from datetime import datetime, timedelta


BUCKET = os.environ.get('S3_BUCKET')
SETTINGS_FILE_KEY = "configuration/settings.json"

s3_client = boto3.client('s3')

def config_update_handler(previous_config, new_config):
    '''Handle scenarios where the configuration is updated. This is invoked by the API when a user updates the days_to_keep_motionless_videos option'''

    print('Inside config update handler!!!')




def handler(event, context):
    print(event)
    if 'previous_config' in event['body'].keys():
        return config_update_handler(event['body']['previous_config'], event['body']['new_config'])

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        config = json.load(settings_file)

    today = datetime.today()

    cutoff_date = today - timedelta(days=config['days_to_keep_motionless_videos'])

    folder_to_delete = f'footage/normal/{cutoff_date.strftime("%Y-%m/%d")}'

    s3_client.delete_object(Bucket=BUCKET, Key=folder_to_delete)

