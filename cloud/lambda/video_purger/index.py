import boto3
import os
from datetime import datetime, timedelta


BUCKET = os.environ.get('S3_BUCKET')
SETTINGS_FILE_KEY = "configuration/settings.json"

s3_client = boto3.client('s3')


def handler(event, context):
    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        config = json.load(settings_file)

    today = datetime.today()

    cutoff_date = today - timedelta(days=config['days_to_keep_motionless_files'])

    folder_to_delete = f'footage/normal/{cutoff_date.strftime("%Y-%m/%d")}'

    client.delete_object(Bucket=BUCKET, Key=folder_to_delete)



# TODO - add logic for when this gets triggered by the api lambda function (which should trigger this whenever the cutoff date is changed to a smaller value)

