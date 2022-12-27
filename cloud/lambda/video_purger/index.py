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
        month_folder = f'footage/normal/{day_to_remove.strftime("%Y-%m")}'
        folder = f'{month_folder}/{day_to_remove.strftime("%d")}'
        folders_to_remove.append(folder)

        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=folder)

        for page in pages:
            if 'Contents' not in page.keys():
                continue

            for obj_data in page['Contents']:
                print(f"deleting: {obj_data['Key']}")
                s3_client.delete_object(Bucket=BUCKET, Key=obj_data['Key'])
        print(f'deleting: {folder}')
        s3_client.delete_object(Bucket=BUCKET, Key=folder)

        res = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=month_folder)
        if res['KeyCount'] == 1:
            print(f'deleting: {month_folder}')
            s3_client.delete_object(Bucket=BUCKET, Key=month_folder)


    return { 'statusCode': 200 }


def handler(event, _):
    if 'previous_config' in event.keys():
        return config_update_handler(event['previous_config'], event['new_config'])

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        config = json.load(settings_file)

    cutoff_date = today - timedelta(days=(config['days_to_keep_motionless_videos'] + 1))
    month_folder = f'footage/normal/{cutoff_date.strftime("%Y-%m")}'
    folder_to_delete = f'{month_folder}/{cutoff_date.strftime("/%d")}'


    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix=folder_to_delete)

    for page in pages:
        if 'Contents' not in page.keys():
            continue

        for obj_data in page['Contents']:
            print(f"deleting: {obj_data['Key']}")
            s3_client.delete_object(Bucket=BUCKET, Key=obj_data['Key'])
    print(f"deleting: {folder_to_delete}")
    s3_client.delete_object(Bucket=BUCKET, Key=folder_to_delete)

    res = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=month_folder)
    if res['KeyCount'] == 1:
        print(f"deleting: {month_folder}")
        s3_client.delete_object(Bucket=BUCKET, Key=month_folder)
