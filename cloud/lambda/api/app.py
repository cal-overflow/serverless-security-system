import boto3
import json
import os
import datetime
import time


BUCKET = os.environ.get('S3_BUCKET')
today = datetime.date.today()
presign_url_expiration_time = int(os.environ.get('PRESIGN_URL_EXPIRATION_TIME'))


def get_files_in_folder(folder, suffix=''):
    s3_client = boto3.client('s3')
    files = []

    # TODO - pagination for when there is more than 1000 objects
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=folder)

    if response is not None and 'Contents' in response.keys():
        for obj_data in response['Contents']:
            if not obj_data['Key'].endswith(suffix):
                continue

            presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': obj_data['Key']}, ExpiresIn=presign_url_expiration_time)
            
            filename = obj_data['Key'].split('/')[-1]
            files.append({
                'filename': filename,
                'video_url': presigned_url,
                'expiration': time.time() + presign_url_expiration_time
            })

    return files


def get_videos_with_motion(date_folder, camera_filter):
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


def get_videos_without_motion(date_folder, camera_filter):
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


# TODO - implement authentication! Auth should be required in order to do all requests


# Handler (API) functions:
def get_videos(event, _):

    # default query parameters
    requested_date = today
    requested_camera = ''

    query_parameters = event['queryStringParameters']

    if query_parameters is not None:
        if 'date' in query_parameters.keys():
            requested_date = datetime.datetime.strptime(query_parameters['date'], '%Y-%m-%d')
        if 'camera' in query_parameters.keys():
            requested_camera = query_parameters['camera']

    videos = None
    
    date_folder = requested_date.strftime('%Y-%m/%d')
    if event['path'].endswith('all'):
        videos_with_motion = get_videos_with_motion(date_folder, requested_camera)
        videos_without_motion = get_videos_without_motion(date_folder, requested_camera)
        videos = videos_with_motion + videos_without_motion
    elif event['path'].endswith('motion'):
        videos = get_videos_with_motion(date_folder, requested_camera)
    elif event['path'].endswith('motionless'):
        videos = get_videos_with_motion(date_folder, requested_camera)

    


    return { 'statusCode': 200, 'body': json.dumps(videos) }

# TODO:
# def get_settings(event, _):

# TODO:
# def update_settings(event, _):
