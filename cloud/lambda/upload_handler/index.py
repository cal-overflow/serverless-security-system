import boto3
import os


bucket_name = os.environ.get('S3_BUCKET')



def handler(event, context):
    '''Handles file uploads from clients. Updates latest information for the client that uploaded the clip.'''

    s3_client = boto3.client("s3")
    
    object_to_process = event['Records'][0]['s3']['object']

    print('event:')
    print(event)

