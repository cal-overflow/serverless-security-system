import boto3
import json
import os

client_properties_that_can_change_by_user_input = [ 'name', 'motion_threshold' ]
BUCKET = os.environ.get('S3_BUCKET')

s3_client = boto3.client('s3')


def get_client_object_key(id):
    '''Returns the object key for the given client id.'''

    return f'configuration/clients/{id}.json'



def get_files_in_folder(folder, suffix=''):
    '''Get all files in a given folder. Optionally, a suffix can be used to filter the results.'''

    keys = []

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix=folder)

    for page in pages:
        for obj_data in page['Contents']:
            if not obj_data['Key'].endswith(suffix):
                continue

            object_key = obj_data['Key']
            keys.append(object_key)

    return keys


def get_all_clients(event, _):
    '''Returns all clients. Requires the authenticated user to be an admin.'''

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    client_file_keys = get_files_in_folder('configuration/clients')
    clients = []

    for client_key in client_file_keys:

        local_file = '/tmp/tmp.json'
        try:
            s3_client.download_file(BUCKET, client_key, local_file)

            with open(local_file) as f:
                clients.append(json.load(f))


        except:
            return { 'statusCode': 500, 'body': json.dumps('An error occurred while fetching some clients') }

    return { 'statusCode': 200, 'body': json.dumps(clients) }


def get_client(event, _):
    '''Returns a client based on the id in the path. Returns None if the client does not exist. Requires the authenticated user to be an admin.'''

    client_to_get = event['rawPath'][len('/clients/'):]

    if '/' in client_to_get or client_to_get == '':
        return { 'statusCode': 400 }

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    local_file = f'/tmp/{client_to_get}.json'
    try:
        s3_client.download_file(BUCKET, get_client_object_key(client_to_get), local_file)

    except:
        return { 'statusCode': 404, 'body': json.dumps('Client does not exist') }

    with open(local_file) as f:
        client = json.load(f)

    return { 'statusCode': 200, 'body': json.dumps(client) }


def update_client(event, _):
    '''Updates the client with the id in the path. Requires the authenticated user to be an admin.'''

    client_to_update = event['rawPath'][len('/clients/'):]

    if '/' in client_to_update or client_to_update == '':
        return { 'statusCode': 400 }

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    client_updates = json.loads(event['body'])

    client_file_key = get_client_object_key(client_to_update)
    
    local_file = f'/tmp/{client_to_update}.json'
    try:
        s3_client.download_file(BUCKET, client_file_key, local_file)

        with open(local_file) as f:
            client = json.load(f)
    except:
        return { 'statusCode': 404, 'body': json.dumps('Client does not exist') }

    try:
        updated_client = { **client }

        for key, val in client_updates.items():
            if key in client_properties_that_can_change_by_user_input:
                updated_client[key] = val

        with open(local_file, 'w') as f:
            json.dump(updated_client, f)

        s3_client.upload_file(local_file, BUCKET, client_file_key)

        return { 'statusCode': 200, 'body': json.dumps(updated_client) }

    except:
        return { 'statusCode': 500, 'body': json.dumps('An error occurred while trying to update the client') }

