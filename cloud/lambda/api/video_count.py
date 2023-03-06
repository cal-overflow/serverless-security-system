import boto3
import json
import os
import datetime
import time


BUCKET = os.environ.get('S3_BUCKET')
PRESIGN_URL_EXPIRATION_TIME = int(os.environ.get('PRESIGN_URL_EXPIRATION_TIME'))
today = datetime.date.today()
current_hour = int(today.strftime('%H'))
s3_client = boto3.client('s3')

# Helper functions
def count_files(prefix, suffix=''):
    '''Count all files with the given prefix. Optionally, a suffix can be used to filter the results.'''

    num_files = 0

    paginator = s3_client.get_paginator('list_objects_v2')
    print(f'counting items with prefix: {prefix}')
    pages = paginator.paginate(Bucket=BUCKET, Prefix=prefix)

    for page in pages:
        if 'Contents' not in page.keys():
            continue

        for obj_data in page['Contents']:
            if not obj_data['Key'].endswith(suffix):
                continue

            num_files += 1

    return num_files


def count_videos_with_motion(requested_month, camera_filter=''):
    '''Count all videos with motion in a given month. Optionally, a camera name can be used as a suffix to filter the results.'''
    month_folder = requested_month.strftime('%Y-%m')
    camera_suffix = f'{camera_filter}.mp4'

    num_videos = count_files(f'footage/activity/{month_folder}', camera_suffix)

    return num_videos


def count_videos_without_motion(requested_month, camera_filter=''):
    '''Count all videos without motion in a given month. Optionally, a camera name can be used as a suffix to filter the results.'''
    month_folder = requested_month.strftime('%Y-%m')
    camera_suffix = f'{camera_filter}.mp4'

    num_videos = count_files(f'footage/normal/{month_folder}', camera_suffix)

    return num_videos


def get_video_count(event, _):
    # default query parameters
    requested_month = today
    requested_camera = ''

    query_parameters = event.get('queryStringParameters', None)

    if query_parameters is not None:
        if 'month' in query_parameters.keys():
            requested_month = datetime.datetime.strptime(query_parameters['date'], '%Y-%m')
        if 'camera' in query_parameters.keys():
            requested_camera = query_parameters['camera']

    num_videos = 0
    
    if event['rawPath'].endswith('count/all'):
        num_videos_with_motion = count_videos_with_motion(requested_month, requested_camera)
        num_videos_without_motion = count_videos_without_motion(requested_month, requested_camera)

        num_videos = num_videos_with_motion + num_videos_without_motion

    elif event['rawPath'].endswith('count/normal'):
        num_videos = count_videos_without_motion(requested_month, requested_camera)

    elif event['rawPath'].endswith('count/activity'):
        num_videos = count_videos_with_motion(requested_month, requested_camera)

    return { 'statusCode': 200, 'body': json.dumps(num_videos) }

