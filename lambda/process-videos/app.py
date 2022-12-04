import boto3
import os
import time
from Video import Video

bucket_name = os.environ.get('S3_BUCKET')
current_time = time.time()
date = time.strftime('%Y-%m-%d', time.localtime(current_time))
folder = f"{date}/"

def handler(event, context):
    print('Inside the lambda!')
    # Make folder to download files locally
    if not os.path.isdir(f'/tmp/{folder}'):
        os.makedirs(f'/tmp/{folder}')

    s3_client = boto3.client("s3")
    # TODO - handle scenarios where there are > 1000 objects in bucket (this is unlikely since we're only getting the things in the "folder")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder)
    s3_objects = response.get("Contents")
    
    total_data_size = 0
    total_videos_deleted = 0
    videos = []
    
    for obj in s3_objects:
        filename = obj['Key']
        s3_client.download_file(bucket_name, filename, '/tmp/{obj["Key"]}')
        total_data_size += obj["Size"]

        videos.append(Video(filename))

    for vid in videos:
        vid.check_for_motion()

        if not vid.contains_motion:
            s3_client.delete_object(Bucket=bucket_name, Key=vid.file)
            total_videos_deleted += 1


    print('Deleted {}/{} videos for {}. Processed {} bytes of video. Deleted {} files.'.format(total_videos_deleted, len(videos), date, total_data_size))
