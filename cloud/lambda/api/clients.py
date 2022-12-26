import boto3
import json
import os


BUCKET = os.environ.get('S3_BUCKET')

s3_client = boto3.client('s3')


def get_client_object_key(id):
    '''Returns the object key for the given client id.'''

    return f'configuration/clients/{id}.json'



def get_files_in_folder(folder, suffix=''):
    '''Get all files in a given folder. Optionally, a suffix can be used to filter the results.'''

    keys = []

    # TODO - pagination for when there is more than 1000 objects
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=folder)

    if response is not None and 'Contents' in response.keys():
        for obj_data in response['Contents']:
            if not obj_data['Key'].endswith(suffix):
                continue

            object_key = obj_data['Key']
            keys.append(object_key)

    return keys



def get_client(event, _):
    '''Returns a client based on the id in the path. Returns None if the client does not exist. Requires the authenticated user to be an admin.'''

    client_to_get = event['rawPath'].strip('/client/').strip('/')

    if '/' in client_to_get or client_to_get == '':
        return { 'statusCode': 400 }

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    local_file = f'/tmp/{client_to_get}.json'
    try:
        s3_client.download_file(BUCKET, get_client_object_key(client_to_get), local_file)

        with open(local_file) as f:
            client = json.load(f)

        return { 'statusCode': 200, 'body': json.dumps(client) }

    except:
        return { 'statusCode': 404, 'body': json.dumps('Client does not exist') }



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


        except Exception as e:
            return { 'statusCode': 500, 'body': json.dumps(f'An error occurred while fetching some clients\nError:\n{e}') }

    return { 'statusCode': 200, 'body': json.dumps(clients) }


def update_client(event, _):
    '''Updates the client with the id in the path. Requires the authenticated user to be an admin.'''

    client_to_update = event['rawPath'].strip('/client/').strip('/')

    if '/' in client_to_update or client_to_update == '':
        return { 'statusCode': 400 }

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    client_updates = json.loads(event['body'])

    client_file_key = get_client_object_key(client_to_update)
    
    local_file = f'/tmp/{client_to_get}.json'
    try:
        s3_client.download_file(BUCKET, client_file_key, local_file)

        with open(local_file) as f:
            client = json.load(f)
    except:
        return { 'statusCode': 404, 'body': json.dumps('Client does not exist') }

    try:
        updated_client = { **client }

        for key, val in client.items():
            if key in client_updates.keys():
                updated_client[key] = client_updates[key]

        with open(local_file, 'w') as f:
            json.dump(updated_client, f)

        s3_client.upload_file(BUCKET, client_file_key, local_file)

        return { 'statusCode': 200, 'body': json.dumps(client) }

    except Exception as e:
        return { 'statusCode': 500, 'body': json.dumps(f'An error occurred while trying to update the client\nError:\n{e}') }

