import boto3
import json
import os
import datetime
import time


FUNCTION_NAME = os.environ.get('FUNCTION_NAME')
BUCKET = os.environ.get('S3_BUCKET')
PRESIGN_URL_EXPIRATION_TIME = int(os.environ.get('PRESIGN_URL_EXPIRATION_TIME'))
SETTINGS_FILE_KEY = "configuration/settings.json"
today = datetime.date.today()

# Helper functions
def get_files_in_folder(folder, suffix=''):
    s3_client = boto3.client('s3')
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


# Video
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


# Configuration
def get_configuration(event, _):
    s3_client = boto3.client('s3')

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        settings = json.load(settings_file)

    settings['presigned_url_expiration_time'] = PRESIGN_URL_EXPIRATION_TIME
    
    return { 'statusCode': 200, 'body': json.dumps(settings) }


def update_configuration(event, _):
    new_configuration = json.loads(event['body'])

    # Validate the new config
    if type(new_configuration['is_motion_outlined']) != bool:
        return { 'statusCode': 400 }
    if type(new_configuration['clip_length']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['clips_per_upload']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['presign_url_expiration_time']) != int:
        return { 'statusCode': 400 }


    s3_client = boto3.client('s3')
    lambda_client = boto3.client('lambda')

    lambda_client.update_function_configuration(
            FunctionName=FUNCTION_NAME,
            Environment={
                'Variables': {
                    'FUNCTION_NAME': FUNCTION_NAME,
                    'S3_BUCKET': BUCKET,
                    'PRESIGN_URL_EXPIRATION_TIME': str(new_configuration['presign_url_expiration_time']),
                }
            }
        )
    
    del new_configuration['presign_url_expiration_time']

    with open('/tmp/output.json', 'w') as output_file:
        json.dump(new_configuration, output_file)

    s3_client.upload_file('/tmp/output.json', BUCKET, SETTINGS_FILE_KEY)

    return { 'statusCode': 201, 'body': event['body'] }



# TODO - implement authentication - Auth should be required in order to do all requests
def handler(event, context):
    print(event)

    print(event['path'])
    print(event['httpMethod'])

    if event['path'].startswith('/videos'):
        if event['httpMethod'] == 'GET':
            return get_videos(event, context)

    elif event['path'].startswith('/configuration'):
        if event['httpMethod'] == 'GET':
            return get_configuration(event, context)
        if event['httpMethod'] == 'POST':
            return update_configuration(event, context)
