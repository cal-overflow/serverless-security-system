# serverless-security-system
A serverless security system built with AWS Services
**NOTE: This project is a work in progress**

### Some notes
**This security system sacrifices "live" streaming for the benefit of a serverless (more affordable) architecture.** Additionally, the removal of livestreaming allows for less cpu requirements of each camera.

#### Archicture (tentative)

##### Client
A "Client" is more-or-less a camera + computer that has the purpose of recording footage and periodically sending it to the cloud storage. \
Little or no video processing is done at the client-side to allow "weak" computers (such as a raspberry pi) to act as the client.

##### Cloud CPU
Cloud computing resources (such as AWS Lambda) will periodically run and process the footage that has been saved by each client. \
Ideally, this process will remove footage that is older than a set number of days, weeks, or months AND has no indication of movement/security concern.

##### Misc notes
- Docker-based client "application" that records footage of x min intervals.
- Some kind of authentication will be needed so that setting up a client to have permissions to upload files to S3 bucket.
- CRON-interval processes where the "client" syncs the footage to an S3 bucket.
- CRON-interval processes at the cloud-level where footage is "processed" and potentially disposed.


## Client software
Linux: Run the client software using docker.
MacOS/Windows: Run the client software using a python virtual environment.

**Note:** This software is intended to be run on linux (i.e., Raspberry Pi). Using docker to run the program becomes [quite challenging on MacOS and Windows machines](https://medium.com/@jijupax/connect-the-webcam-to-docker-on-mac-or-windows-51d894c44468). \

### Using docker
#### Requirements
- Docker

```bash
$ docker run <image name>
```
To use the latest docker image, simply replace `<image name>` with `caloverflow/security-system-client:latest` \
View all available docker images on the [Docker Hub repository](https://hub.docker.com/repository/docker/caloverflow/security-system-client). 

### Using Python virtualenv
#### Requirements
- Python 3.9 or 3.10
- pip

#### Create virtual environment and install dependencies
```bash
$ python -m venv ./venv
$ pip install -r requirements.txt
```

#### Run the program
```bash
# Activate the virtual environment
$ source ./venv/bin/active

# Run the script
$ python src/main.py
```

#### Environment variables
The following environment variables may be defined to override the default options

| Variable | Default | Purpose |
| :-: | :-: | :--|
| `CLIP_LENGTH` | `30` | The length, in seconds, that clips should be saved. |
| `OUTPUT_PATH` | `./tmp` | The path to the folder where video clips should be saved. |

Pass the environment variables via the command line:
##### Docker
```bash
$ docker run <image name> -e <ENV_VARIABLE>=<DESIRED_VALUE>
```

##### Python command line
```bash
$ <ENV_VARIABLE>=<DESIRED_VALUE> python src/main.py
```

