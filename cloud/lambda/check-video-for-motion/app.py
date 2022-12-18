import boto3
import os
import time
from Video import Video

bucket_name = os.environ.get('S3_BUCKET')
processed_video_output_folder = os.environ.get('PROCESSED_VIDEOS_FOLDER')


def handler(event, context):
    s3_client = boto3.client("s3")
    
    object_to_process = event['Records'][0]['s3']['object']
    object_key = object_to_process['key']
    date, clip_start_time, camera_name = object_key.strip('.mp4').split('_')
    filename = object_key.split('/')[-1]
    local_file_path = f'/tmp/{filename}'

    s3_client.download_file(bucket_name, object_key, local_file_path)
    
    vid = Video(local_file_path)
    vid.check_for_motion()

    if not vid.contains_motion:
        print(f'Video {object_key} does not contain motion')
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print(f'Deleted video {object_key}')
    else:
        year, month, day = object_key.split('/')[1].split('-')
        new_object_key = os.path.relpath(f'{processed_video_output_folder}/{year}/{month}/{day}/{clip_start_time}-{camera_name}.mp4')
        s3_client.upload_file(vid.processed_file, bucket_name, new_object_key, ExtraArgs={'ContentType': "video/mp4"})
        print(f'Saved video {new_object_key}')

        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print(f'Deleted video {object_key}')


    # Remove local files (otherwise lambda runner may run out of storage)
    try:
        os.remove(local_file_path)
    except:
        pass
    try:
        os.remove(vid.processed_file)
    except:
        pass

