import boto3
import os
import time
from Video import Video

bucket_name = os.environ.get('S3_BUCKET')


def handler(event, context):
    s3_client = boto3.client("s3")
    
    object_to_process = event['Records'][0]['s3']['object']
    object_key = object_to_process['key']
    filename = object_key.split('/')[-1]
    local_file_path = f'/tmp/{filename}'

    print(f'Downloading {object_key} to {local_file_path}')
    s3_client.download_file(bucket_name, object_key, local_file_path)
    
    # Perform the video processing here so we can delete it and continue on to the next (minimize storage use)
    vid = Video(local_file_path)
    vid.check_for_motion()

    if not vid.contains_motion:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print('Deleted video from S3 bucket')

