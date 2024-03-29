import boto3
import json
import os
import time
import uuid
import re
from decimal import Decimal


USERS_TABLE= os.environ.get('USERS_TABLE')
PROJECTION_EXPRESSSION='#n, #a'
EXPRESSION_ATTRIBUTE_NAMES={ '#n': 'name', '#a': 'admin', }
ACCEPTED_KEYS=['name', 'admin', 'pin']
username_pattern = re.compile("^([a-zA-Z0-9_-]){3,24}$")


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(USERS_TABLE)


def delete_user(event, _):
    '''Deletes a user based on the Username in the path. Requires the authenticated user to be an admin.'''

    if not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    user_to_delete = event['rawPath'][len('/users/'):]

    if '/' in user_to_delete or user_to_delete == '':
        return { 'statusCode': 400 }


    table.delete_item(Key={ 'name': user_to_delete })

    return { 'statusCode': 200, 'body': json.dumps('User successfully deleted') }


def get_user(event, _):
    '''Returns a user based on the Username in the path. Returns None if the user does not exist. Requires the authenticated user to be an admin (or the requested user).'''

    user_to_get = event['rawPath'][len('/users/'):]

    if '/' in user_to_get or user_to_get == '':
        return { 'statusCode': 400 }

    if event['authenticated_user']['name'] != user_to_get and not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    response = table.get_item(
            Key={ 'name': user_to_get },
            ProjectionExpression=PROJECTION_EXPRESSSION + ', #p',
            ExpressionAttributeNames={
                **EXPRESSION_ATTRIBUTE_NAMES,
                '#p': 'pin'
            },
        )

    if 'Item' not in response.keys():
        return { 'statusCode': 404, 'body': json.dumps('User does not exist') }

    return { 'statusCode': 200, 'body': json.dumps(response['Item']) }


def get_all_users(event, _):
    '''Returns a user (based on the given user name). Returns None if the user does not exist.'''

    response = table.scan(
            ProjectionExpression=PROJECTION_EXPRESSSION,
            ExpressionAttributeNames=EXPRESSION_ATTRIBUTE_NAMES
        )

    return { 'statusCode': 200, 'body': json.dumps(response['Items']) }


def update_user(event, _):
    '''Updates the user with the Username in the path. Requires the authenticated user to be an admin (or the user being updated).'''

    user_to_update = event['rawPath'][len('/users/'):]

    if '/' in user_to_update or user_to_update == '':
        return { 'statusCode': 400 }

    if event['authenticated_user']['name'] != user_to_update and not event['authenticated_user']['admin']:
        return { 'statusCode': 403 }

    
    response = table.get_item(Key={ 'name': user_to_update })

    if 'Item' not in response.keys():
        return { 'statusCode': 404, 'body': json.dumps('User does not exist') }

    db_user = response['Item']

    user_updates = json.loads(event.get('body', '{}'))
    if len(user_updates.keys()) == 0:
        return { 'statusCode': 400, 'body': json.dumps('Expected a payload') }

    if not event['authenticated_user']['admin'] and 'admin' in user_updates.keys():
        return { 'statusCode': 403 }


    delete_old_entry = False
    
    if 'name' in user_updates.keys():
        if not username_pattern.match(user_updates['name']):
            return { 'statusCode': 400 , 'body': json.dumps('Invalid name') }

        db_response_with_name = table.get_item(Key={ 'name': user_updates['name'] })
        if 'Item' in db_response_with_name:
            return { 'statusCode': 409 , 'body': json.dumps('A user with the requested name already exists') }

        # wipe out the old user once their new entry is entered
        delete_old_entry = True


    updated_db_user = {
        **db_user,
        **user_updates,
    }

    # TODO - handle response code given the item is not created/updated (put)
    table.put_item(Item=updated_db_user)

    if delete_old_entry:
        table.delete_item(Key={ 'name': user_to_update })

    response = table.get_item(
        Key={ 'name': updated_db_user['name'] },
        ProjectionExpression=PROJECTION_EXPRESSSION,
        ExpressionAttributeNames=EXPRESSION_ATTRIBUTE_NAMES
    )

    return { 'statusCode': 200, 'body': json.dumps(response['Item']) }

