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
def get_files(prefix, suffix=''):
    '''Get all files with the given prefix. Optionally, a suffix can be used to filter the results.'''

    files = []

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix=prefix)

    for page in pages:
        for obj_data in page['Contents']:
            if not obj_data['Key'].endswith(suffix):
                continue

            presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': obj_data['Key']}, ExpiresIn=PRESIGN_URL_EXPIRATION_TIME)
            
            filename = obj_data['Key'].split('/')[-1]
            files.append({
                'filename': filename,
                'video_url': presigned_url,
                'expiration': time.time() + PRESIGN_URL_EXPIRATION_TIME
            })

    return files


def get_videos_with_motion(requested_date, requested_hours, camera_filter=''):
    '''Get a list of all videos with motion in a given date and within the requested hours. Optionally, a camera name can be used as a suffix to filter the results.'''
    date_folder = requested_date.strftime('%Y-%m/%d')
    camera_suffix = f'{camera_filter}.mp4'

    videos = []

    for hour in requested_hours:
        folder = f'footage/activity/{date_folder}/{hour:02d}'
        videos += get_files(folder, camera_suffix)

    for video in videos:
        video_start_time, camera_name = video['filename'][:-4].split('_')
        del video['filename']
        video['camera'] = camera_name
        video['time'] = video_start_time
        video['contains_motion'] = True

    return videos


def get_videos_without_motion(requested_date, requested_hours, camera_filter):
    '''Get a list of all videos without motion in a given date and within the requested hours. Optionally, a camera name can be used as a suffix to filter the results.'''
    date_folder = requested_date.strftime('%Y-%m/%d')
    camera_suffix = f'{camera_filter}.mp4'

    videos = []

    for hour in requested_hours:
        folder = f'footage/normal/{date_folder}/{hour:02d}'
        videos += get_files(folder, camera_suffix)

    for video in videos:
        video_start_time, camera_name = video['filename'][:-4].split('_')
        del video['filename']
        video['camera'] = camera_name
        video['time'] = video_start_time
        video['contains_motion'] = False

    return videos


def get_videos(event, _):
    videos = []

    # default query parameters
    requested_date = today
    requested_camera = ''
    requested_hours = [ list(range(0, 24)) ]

    query_parameters = event.get('queryStringParameters', None)

    if query_parameters is not None:
        if 'date' in query_parameters.keys():
            requested_date = datetime.datetime.strptime(query_parameters['date'], '%Y-%m-%d')
        if 'camera' in query_parameters.keys():
            requested_camera = query_parameters['camera']
        if 'hours' in query_parameters.keys():
            requested_hours_str = query_parameters['hours'].split('-')
            if len(requested_hours_str) != 2:
                return { 'statusCode': 400, 'body': json.dumps('Invalid hours parameter') }

            start_hour = int(requested_hours_str[0])
            end_hour = int(requested_hours_str[1])

            requested_hours = [list(range(start_hour, end_hour + 1))]

    
    if event['rawPath'].endswith('/all'):
        videos_with_motion = get_videos_with_motion(requested_date, requested_hours, requested_camera)
        videos_without_motion = get_videos_without_motion(requested_date, requested_hours, requested_camera)

        videos = videos_with_motion + videos_without_motion
        videos = sorted(videos, key=lambda video: video['time'])

    elif event['rawPath'].endswith('/motion'):
        videos = get_videos_with_motion(requested_date, requested_hours, requested_camera)

    elif event['rawPath'].endswith('/motionless'):
        videos = get_videos_with_motion(requested_date, requested_hours, requested_camera)

    


    return { 'statusCode': 200, 'body': json.dumps(videos) }

