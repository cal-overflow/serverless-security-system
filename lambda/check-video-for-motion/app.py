import boto3
import os
import time
from Video import Video

bucket_name = os.environ.get('S3_BUCKET')
current_time = time.time()
date = time.strftime('%Y-%m-%d', time.localtime(current_time))
folder = f"{date}/"

def handler(event, context):
    print('IN LAMBDA - TODO: process the video here')
    print(event)
    return
    # # Make folder to download files locally
    # if not os.path.isdir(f'tmp/{folder}'):
    #     os.makedirs(f'/tmp/{folder}')

    # s3_client = boto3.client("s3")

    # # TODO - download the file and check if it contains motion
    # # filename = obj['Key']
    # # file_path = f'/tmp/{filename}'
    # # s3_client.download_file(bucket_name, filename, file_path)
    # 
    # # Perform the video processing here so we can delete it and continue on to the next (minimize storage use)
    # vid = Video(file_path)
    # vid.check_for_motion()
    # videos.append(vid)

    # # if not vid.contains_motion:
    # #     s3_client.delete_object(Bucket=bucket_name, Key=vid.file)
    # #     total_videos_deleted += 1

