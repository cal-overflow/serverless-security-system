# API
The API (backend) for the application utilizes AWS Serverless functions to reduce costs when serving content.

The various endpoints are documented below. Note that these are rough notes and may not be a very reliable representation of the API.


## Videos (footage)
All `/videos` endpoints accept the following query parameters:
- `date` -  A specific day to filter. Defaults to the current date (for wherever the Lambda function is running).
- `hours` - A range of hours to filter. Defaults to hours 0 through 23, which can result in a slow response time.
- `camera` - A specific camera (client) id to filter.

### GET `/videos/all`
Return all video footage
### GET `/videos/activity`
Return only video footage with motion (activity)
### GET `/videos/normal`
Return only video footage with no motion (normal)

## Video Count
A special endpoint for retrieving the number of videos saved for a given month. \
All `/video-count` endpoints accept the following query parameters:
- `date` -  A specific month to filter. Defaults to the current month (for wherever the Lambda function is running).
- `camera` - A specific camera (client) id to filter.

### GET `/video-count/all`
Return the number of all video footage stored for the requested month
### GET `/video-count/activity`
Return the number of video footage with activity stored for the requested month
### GET `/video-count/normal`
Return the number of video footage without activity stored for the requested month

## Authentication
### POST `/auth/login`
Returns an access token that can be used to make other requests to the API. \
Example body:
```json
{
  "name": "christian",
  "pin": "123abc"
}
```
Example response:
```json
{
  "token": "e0a84ef9e781436bbc774286c7b3d0d5",
  "token_expiration": "1672533351.0030391216278076171875"
}
```

### POST `/auth/refresh`
Return a fresh access token. This request does not require a body. All that is needed is the `access-token` passed in the header.

The response will follow the same format as one returned from the `/auth/login` endpoint.

### POST `/auth/logout`
Revokes the user's current access token.


## Config
### GET `/config`
**Requires Admin priviliges** \
Returns the system configuration. \
Example response:
```json
{
  "is_motion_outlined": false,
  "clip_length": 60,
  "clips_per_upload": 1,
  "presign_url_expiration_time": 3600,
  "default_motion_threshold": 5000,
  "days_to_keep_motionless_videos": 3
}
```

### POST `/config`
**Requires Admin priviliges** \
Updates the system configuration. Returns the updated system configuration. 



## Users
### GET `/users`
**Requires Admin priviliges** \
Returns a list of all users. \
Example response:
```json
[
  {
    "name": "christian",
    "pin": "123abc",
    "admin": "true"
  }
]
```

### POST `/users`
**Requires Admin priviliges** \
Create a new user. \
Example body:
```json
{
  "name": "christian",
  "pin": "123abc",
  "admin": "true"
}
```

### GET `/users/{username}`
**Requires Admin priviliges** for getting users other than oneself .
Returns the user data
Example response for `/users/christian`:
```json
{
  "name": "christian",
  "pin": "123abc",
  "admin": "true"
}
```

### PATCH `/users/{username}`
**Requires Admin priviliges** for updating users other than oneself.
Updates a user. Only requires fields that are being changed. \
Example body for changing user `christian`'s name to `steve` with PATCH `/users/christian`:
```json
{
  "name": "steve"
}
```

### DELETE `/users/{username}`
**Requires Admin priviliges** \
Permanently deletes a user \
Example response:
```text
User successfully deleted
```


## Clients
### GET `/clients`
Returns a list of all clients. \
Example response:
```json
[
  {
    "name": "Living Room",
    "id": "1a2b3c",
    "motion_threshold": 5000,
    "last_upload_key": "footage/normal/2023-1/14/04-36-00_1a2b3c.mp4",
    "last_upload_time": 1673670960,
    "is_active": true
  }
]
```


### GET `/clients/{client_id}`
Returns the client data. \
Example response for `/client/1a2b3c`:
```json
{
  "name": "Living Room",
  "id": "1a2b3c",
  "motion_threshold": 5000,
  "last_upload_key": "footage/normal/2023-1/14/04-36-00_1a2b3c.mp4",
  "last_upload_time": 1673670960,
  "is_active": true
}
```

### PATCH `/clients/{client_id}`
**Requires Admin priviliges** \
Updates a client. Only `name` and `motion_threshold` fields are allowed. \
Example body and response for changing client `1a2b3c`'s motion threshold to 3500 via PATCH `/client/1a2b3c`:
Body:
```json
{
  "motion_threshold": 3500
}
```
Response:
```json
{
  "name": "Living Room",
  "id": "1a2b3c",
  "motion_threshold": 3500,
  "last_upload_key": "footage/normal/2023-1/14/04-36-00_1a2b3c.mp4",
  "last_upload_time": 1673670960,
  "is_active": true
}
```

