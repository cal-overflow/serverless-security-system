import boto3
import os
import json
from datetime import datetime

BUCKET = os.environ.get('S3_BUCKET')
SETTINGS_FILE_KEY='configuration/settings.json'
s3_client = boto3.client("s3")


def get_config():
    '''Get the system configuration. Retrieves the settings file from S3.'''

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        settings = json.load(settings_file)

    return settings


def handler(event, _):
    '''Handles file uploads from clients. Updates latest information for the client that uploaded the clip.'''

    record = event['Records'][0]

    object_key = record['s3']['object']['key']
    event_time = datetime.strptime(record['eventTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    event_epoch_time = (event_time - datetime(1970, 1, 1)).total_seconds()


    client = {
        'id': object_key.split('_')[-1][:-4],
        'last_upload_key': object_key,
        'last_upload_time': event_epoch_time,
        'is_active': True
    }

    client_object_key = f'configuration/clients/{client["id"]}.json'

    try:
        s3_client.download_file(BUCKET, client_object_key, '/tmp/client.json')
        
        with open('/tmp/client.json') as client_file:
            existing_client_data = json.load(client_file)

        client = {
            **existing_client_data,
            **client,
        }
    except:
        system_config = get_config()

        client['name'] = 'Unnamed'
        client['motion_threshold'] = system_config['default_motion_threshold']
        pass

    with open('/tmp/client.json', 'w') as updated_client_file:
        json.dump(client, updated_client_file)

    s3_client.upload_file('/tmp/client.json', BUCKET, client_object_key)

