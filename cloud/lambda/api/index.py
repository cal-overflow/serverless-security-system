from auth import get_authenticated_user, get_authenticated_user_api_call, login, logout, refresh_token, create_invitation, accept_invitation
from config import get_config, update_config
from users import delete_user, get_all_users, get_user, update_user
from clients import get_all_clients, get_client, update_client
from videos import get_videos
from video_count import get_video_count


def handler(event, context):
    '''Handles user authentication and routes traffic to its appropriate handler.'''

    method = event['requestContext']['http']['method']
    print(f"{method} {event['rawPath']}") # TODO - probably delete

    invalid_request_method = False

    if event['rawPath'].startswith('/auth'):
        if event['rawPath'].startswith('/auth/invitations'):
            if method == 'POST':
                return create_invitation(event, context)
            if method == 'PUT':
                return accept_invitation(event, context)
            else:
                invalid_request_method = True
        if method == 'POST':
            if event['rawPath'].startswith('/auth/login'):
                return login(event, context)
            if event['rawPath'].startswith('/auth/refresh'):
                return refresh_token(event, context)
            if event['rawPath'].startswith('/auth/logout'):
                return logout(event, context)
        elif method == 'GET':
            if event['rawPath'].startswith('/auth/user'):
                return get_authenticated_user_api_call(event, context)

        invalid_request_method = False


    authenticated_user = get_authenticated_user(event, context)
    event['authenticated_user'] = authenticated_user


    if event['rawPath'] == '/':
        return { 'statusCode': 200 }

    # below API calls require authentication
    if authenticated_user is None:
        return { 'statusCode': 401 }



    if event['rawPath'].startswith('/videos'):
        if method == 'GET':
            return get_videos(event, context)
        else:
            invalid_request_method = True

    elif event['rawPath'].startswith('/video-count'):
        if method == 'GET':
            return get_video_count(event, context)
        else:
            invalid_request_method = True

    elif event['rawPath'].startswith('/config'):
        if method == 'GET':
            return get_config(event, context)
        elif method == 'POST':
            return update_config(event, context)
        else:
            invalid_request_method = True

    elif event['rawPath'].startswith('/users'):
        contains_user_name_in_path = len(event['rawPath'].strip('/users')) > 1
        
        if contains_user_name_in_path:
            if method == 'GET':
                return get_user(event, context)
            elif method == 'PATCH':
                return update_user(event, context)
            elif method == 'DELETE':
                return delete_user(event, context)
            else:
                invalid_request_method = True
        else:
            if method == 'GET':
                return get_all_users(event, context)
            elif method == 'POST':
                return create_user(event, context)
            else:
                invalid_request_method = True
   
    elif event['rawPath'].startswith('/clients'):
        contains_id_in_path = len(event['rawPath'].strip('/clients')) > 1
        
        if contains_id_in_path:
            if method == 'GET':
                return get_client(event, context)
            elif method == 'PATCH':
                return update_client(event, context)
            else:
                invalid_request_method = True
        else:
            if method == 'GET':
                return get_all_clients(event, context)
            else:
                invalid_request_method = True

    return { 'statusCode': 405 if invalid_request_method else 400 }

