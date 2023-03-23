import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import time
import uuid
from decimal import Decimal
from users import username_pattern


USERS_TABLE= os.environ.get('USERS_TABLE')
USER_INVITATION_EXPIRATION_TIME = int(os.environ.get('INVITATION_EXPIRATION_TIME'))
USER_TOKEN_EXPIRATION_TIME = int(os.environ.get('USER_TOKEN_EXPIRATION_TIME'))
PROJECTION_EXPRESSSION='#n, #a, #t, #e'
EXPRESSION_ATTRIBUTE_NAMES={ '#n': 'name', '#a': 'admin', '#t': 'token', '#e': 'token_expiration' }

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(USERS_TABLE)


def get_authenticated_user(event, _):
    '''Returns the authenticated user (based on the given access token). Returns None if the user is not authenticated.'''

    token = event['headers'].get('access-token', None)

    if token is None:
        return None


    response = table.query(
        IndexName='TokenIndex',
        KeyConditionExpression=Key('token').eq(token),
        Limit=1,
        ProjectionExpression=PROJECTION_EXPRESSSION,
        ExpressionAttributeNames=EXPRESSION_ATTRIBUTE_NAMES
    )


    if len(response['Items']) == 0:
        return None

    authorized_user = response['Items'][0]

    if authorized_user['token_expiration'] < time.time():
        return None

    return authorized_user

def get_authenticated_user_api_call(event, _):
    '''Returns the authenticated user (based on the given access token). Returns a 400 if the authenticated user cannot be found for any reason.'''

    authenticated_user = get_authenticated_user(event, _)

    if authenticated_user is None:
        return { 'statusCode': 400 }

    return {
        'statusCode': 200,
        'body': json.dumps({
            **authenticated_user,
            'token_expiration': float(authenticated_user['token_expiration'])
        })
    }


def login(event, _):
    '''Generates, stores, and returns an auth token for the associated user (based on the given credentials).Returns an informative message given the input is invalid.'''

    payload = json.loads(event.get('body', '{}'))
    if len(payload.keys()) == 0:
        return { 'statusCode': 400, 'body': json.dumps('Expected a payload') }

    name = payload['name']
    pin = payload['pin']

    response = table.get_item(Key={ 'name': name })

    if 'Item' not in response.keys():
        return { 'statusCode': 400, 'body': json.dumps('User does not exist') }
    
    db_user = response['Item']

    if pin != db_user['pin']:
        return { 'statusCode': 400, 'body': json.dumps('Incorrect pin') }
    
    new_token = uuid.uuid4().hex
    token_expiration = time.time() + USER_TOKEN_EXPIRATION_TIME

    updated_db_user = {
        **db_user,
        'token': new_token,
        'token_expiration': Decimal(token_expiration)
    }

    # TODO - handle response code given the item is not updated
    table.put_item(Item=updated_db_user)

    return {
        'statusCode': 200,
        'body': json.dumps({ 'access_token': new_token, 'token_expiration': token_expiration })
    }


def logout(event, _):
    '''Invalidates the authenticated user's current auth token.'''

    token = event['headers'].get('access-token', None)

    if token is None:
        return { 'statusCode': 403 }

    response = table.query(
        IndexName='TokenIndex',
        KeyConditionExpression=Key('token').eq(token),
        Limit=1
    )


    if len(response['Items']) == 0:
        return { 'statusCode': 500, 'body': json.dumps('Something went wrong fetching your information from the database.') }

    updated_db_user = {
        **response['Items'][0],
        'token_expiration': Decimal(time.time()) # Token is expired right now
    }

    # TODO - handle response code given the item is not updated
    table.put_item(Item=updated_db_user)

    return {
        'statusCode': 200,
        'body': json.dumps('Logout successful')
    }


def refresh_token(event, _):
    '''Generates and returns a new access token for the authenticated user. The user's previous access token becomes invalid.'''

    authenticated_user = get_authenticated_user(event, _)

    if authenticated_user is None:
        return { 'statusCode': 401 }

    new_token = uuid.uuid4().hex
    token_expiration = time.time() + USER_TOKEN_EXPIRATION_TIME

    updated_db_user = {
        **authenticated_user,
        'token': new_token,
        'token_expiration': Decimal(token_expiration)
    }

    # TODO - handle response code given the item is not updated
    table.put_item(Item=updated_db_user)

    return {
        'statusCode': 200,
        'body': json.dumps({ 'access_token': new_token, 'token_expiration': token_expiration })
    }


def create_invitation(event, _):
    '''Creates a user invitation. Returns the temporary invitation token. Requires the authenticated user to be an admin.'''
    
    authenticated_user = get_authenticated_user(event, _)

    if authenticated_user is None:
        return { 'statusCode': 401 }

    if not authenticated_user['admin']:
        return { 'statusCode': 403 }

    token_expiration = time.time() + USER_INVITATION_EXPIRATION_TIME
    invite_token = uuid.uuid4().hex

    new_db_user = {
        'name': f'INVITATION-{uuid.uuid4().hex}',
        'admin': False,
        'token': invite_token,
        'token_expiration': Decimal(token_expiration),
    }

    # TODO - handle response code given the item is not created (put)
    table.put_item(Item=new_db_user)
    
    return { 'statusCode': 200, 'body': json.dumps({ 'invite_token': invite_token, 'token_expiration': token_expiration }) }


def accept_invitation(event, _):
    '''Accepts an invitation corresponding to the given token.'''
    
    invite_token = event['headers'].get('access-token', None)

    response = table.query(
        IndexName='TokenIndex',
        KeyConditionExpression=Key('token').eq(invite_token),
        Limit=1,
        ProjectionExpression=PROJECTION_EXPRESSSION,
        ExpressionAttributeNames=EXPRESSION_ATTRIBUTE_NAMES
    )

    if 'Items' not in response.keys() or len(response['Items']) == 0:
        return { 'statusCode': 404, 'body': json.dumps('Invitation not found') }

    db_user = response['Items'][0]

    if not db_user['name'].startswith('INVITATION-'):
        return { 'statusCode': 500 }
        

    new_user = json.loads(event.get('body', '{}'))
    if len(new_user.keys()) == 0:
        return { 'statusCode': 400, 'body': json.dumps('Expected a payload') }

    if 'admin' in new_user.keys():
        return { 'statusCode': 403 }


    if 'pin' not in new_user.keys():
        return { 'statusCode': 400, 'body': json.dumps('Invalid pin') }

    if 'name' in new_user.keys():
        db_response_with_name = table.get_item(Key={ 'name': new_user['name'] })
        if 'Item' in db_response_with_name:
            return { 'statusCode': 409 , 'body': json.dumps('A user with the requested name already exists') }

    else:
        return { 'statusCode': 400, 'body': json.dumps('Expected a name') }

    updated_db_user = {
        **db_user,
        **new_user,
    }

    # TODO - handle response code given the item is not created/updated (put)
    table.put_item(Item=updated_db_user)

    # Delete the invitation entry
    table.delete_item(Key={ 'name': db_user['name'] })

    response = table.get_item(
        Key={ 'name': updated_db_user['name'] },
        ProjectionExpression=PROJECTION_EXPRESSSION,
        ExpressionAttributeNames=EXPRESSION_ATTRIBUTE_NAMES
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            **response['Item'],
            'token_expiration': float(response['Item']['token_expiration'])
        })
    }

