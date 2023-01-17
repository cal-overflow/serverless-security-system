import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import time
import uuid
from decimal import Decimal


USERS_TABLE= os.environ.get('USERS_TABLE')
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
