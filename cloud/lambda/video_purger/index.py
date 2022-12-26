import boto3
import os
import json
from datetime import datetime, timedelta


BUCKET = os.environ.get('S3_BUCKET')
SETTINGS_FILE_KEY = "configuration/settings.json"

today = datetime.today()
s3_client = boto3.client('s3')

def config_update_handler(previous_config, new_config):
    '''Handle scenarios where the configuration is updated. This is invoked by the API when a user updates the days_to_keep_motionless_videos option'''

    folders_to_remove = []
    for n in list(range(new_config['days_to_keep_motionless_videos'], previous_config['days_to_keep_motionless_videos'] + 1)):
        day_to_remove = today - timedelta(days=n)
        folder = f'footage/normal/{day_to_remove.strftime("%Y-%m/%d")}'
        folders_to_remove.append(folder)

    for folder in folders_to_remove:
        s3_client.delete_object(Bucket=BUCKET, Key=folder)


    return { 'statusCode': 200 }


def handler(event, _):
    if 'previous_config' in event.keys():
        return config_update_handler(event['previous_config'], event['new_config'])

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        config = json.load(settings_file)

    cutoff_date = today - timedelta(days=(config['days_to_keep_motionless_videos'] + 1))
    folder_to_delete = f'footage/normal/{cutoff_date.strftime("%Y-%m/%d")}'

    s3_client.delete_object(Bucket=BUCKET, Key=folder_to_delete)

