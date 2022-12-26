import boto3
import json
import os

BUCKET = os.environ.get('S3_BUCKET')
USERS_TABLE = os.environ.get('USERS_TABLE')
PRESIGN_URL_EXPIRATION_TIME = int(os.environ.get('PRESIGN_URL_EXPIRATION_TIME'))
USER_TOKEN_EXPIRATION_TIME = os.environ.get('USER_TOKEN_EXPIRATION_TIME')
FUNCTION_NAME = os.environ.get('FUNCTION_NAME')
VIDEO_PURGER_FUNCTION_NAME = os.environ.get('VIDEO_PURGER_FUNCTION_NAME')
SETTINGS_FILE_KEY = "configuration/settings.json"


# Configuration
def get_config(event, _):
    '''Get the system configuration. Retrieves the settings file from S3 and attaches the PRESIGN_URL_EXPIRATION_TIME (lambda) environment variable.'''

    s3_client = boto3.client('s3')

    s3_client.download_file(BUCKET, SETTINGS_FILE_KEY, '/tmp/settings.json')

    with open('/tmp/settings.json') as settings_file:
        settings = json.load(settings_file)

    settings['presign_url_expiration_time'] = PRESIGN_URL_EXPIRATION_TIME
    
    return { 'statusCode': 200, 'body': json.dumps(settings) }


def update_config(event, _):
    '''Update the system configuration. Overwrites the settings file in S3 and updates the PRESIGN_URL_EXPIRATION_TIME (lambda) environment variable. Requires the authenticated user to be an admin.'''

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    new_configuration = json.loads(event.get('body', '{}'))
    if len(new_configuration.keys()) == 0:
        return { 'statusCode': 400, 'body': json.dumps('Expected payload') }

    # Validate the new config
    if type(new_configuration['is_motion_outlined']) != bool:
        return { 'statusCode': 400 }
    if type(new_configuration['clip_length']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['clips_per_upload']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['presign_url_expiration_time']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['default_motion_threshold']) != int:
        return { 'statusCode': 400 }
    if type(new_configuration['days_to_keep_motionless_videos']) != int:
        return { 'statusCode': 400 }

    s3_client = boto3.client('s3')

    old_configuration = json.loads(get_config(event, _)['body'])

    lambda_client = boto3.client('lambda')

    lambda_client.update_function_configuration(
            FunctionName=FUNCTION_NAME,
            Environment={
                'Variables': {
                    'S3_BUCKET': BUCKET,
                    'USERS_TABLE': USERS_TABLE,
                    'PRESIGN_URL_EXPIRATION_TIME': str(new_configuration['presign_url_expiration_time']),
                    'USER_TOKEN_EXPIRATION_TIME': USER_TOKEN_EXPIRATION_TIME,
                    'FUNCTION_NAME': FUNCTION_NAME,
                    'VIDEO_PURGER_FUNCTION_NAME': VIDEO_PURGER_FUNCTION_NAME,
                }
            }
        )
    
    del new_configuration['presign_url_expiration_time']

    with open('/tmp/output.json', 'w') as output_file:
        json.dump(new_configuration, output_file)

    s3_client.upload_file('/tmp/output.json', BUCKET, SETTINGS_FILE_KEY)

    if new_configuration['days_to_keep_motionless_videos'] < old_configuration['days_to_keep_motionless_videos']:
        print('invoking video purger lambda function') # TODO - delete

        lambda_client.invoke(
            FunctionName=VIDEO_PURGER_FUNCTION_NAME,
            Payload=json.dumps({
                'previous_config': old_configuration,
                'new_config': new_configuration
            }),
        )

    return { 'statusCode': 200, 'body': event['body'] }

