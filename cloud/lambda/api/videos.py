import boto3
import json
import os
import datetime
import time


BUCKET = os.environ.get('S3_BUCKET')
PRESIGN_URL_EXPIRATION_TIME = int(os.environ.get('PRESIGN_URL_EXPIRATION_TIME'))
today = datetime.date.today()
s3_client = boto3.client('s3')

# Helper functions
def get_files_in_folder(folder, suffix=''):
    '''Get all files in a given folder. Optionally, a suffix can be used to filter the results.'''
    files = []

    # TODO - pagination for when there is more than 1000 objects
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=folder)

    if response is not None and 'Contents' in response.keys():
        for obj_data in response['Contents']:
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


def get_videos_with_motion(requested_date, camera_filter=''):
    '''Get a list of all videos with motion in a given date. Optionally, a camera name can be used as a suffix to filter the results.'''
    date_folder = requested_date.strftime('%Y-%m/%d')
    folder = f'footage/activity/{date_folder}'
    camera_suffix = f'{camera_filter}.mp4'

    videos = get_files_in_folder(folder, camera_suffix)

    for video in videos:
        video_start_time, camera_name = video['filename'][:-4].split('_')
        del video['filename']
        video['camera'] = camera_name
        video['time'] = video_start_time
        video['contains_motion'] = True

    return videos


def get_videos_without_motion(requested_date, camera_filter):
    '''Get a list of all videos without motion in a given date. Optionally, a camera name can be used as a suffix to filter the results.'''
    date_folder = requested_date.strftime('%Y-%m/%d')
    folder = f'footage/normal/{date_folder}'
    camera_suffix = f'{camera_filter}.mp4'

    videos = get_files_in_folder(folder, camera_suffix)

    for video in videos:
        video_start_time, camera_name = video['filename'][:-4].split('_')
        del video['filename']
        video['camera'] = camera_name
        video['time'] = video_start_time
        video['contains_motion'] = False

    return videos


# Video
def get_videos(event, _):
    videos = []

    # default query parameters
    requested_date = today
    requested_camera = ''

    query_parameters = event.get('queryStringParameters', None)

    if query_parameters is not None:
        if 'date' in query_parameters.keys():
            requested_date = datetime.datetime.strptime(query_parameters['date'], '%Y-%m-%d')
        if 'camera' in query_parameters.keys():
            requested_camera = query_parameters['camera']
    
    if event['rawPath'].endswith('/all'):
        videos_with_motion = get_videos_with_motion(requested_date, requested_camera)
        videos_without_motion = get_videos_without_motion(requested_date, requested_camera)

        videos = videos_with_motion + videos_without_motion
        videos = sorted(videos, key=lambda video: video['time'])

    elif event['rawPath'].endswith('/motion'):
        videos = get_videos_with_motion(requested_date, requested_camera)

    elif event['rawPath'].endswith('/motionless'):
        videos = get_videos_with_motion(requested_date, requested_camera)

    


    return { 'statusCode': 200, 'body': json.dumps(videos) }

