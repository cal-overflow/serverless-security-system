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

**Note:** This software is intended to be run on linux (i.e., Raspberry Pi). Using docker to run the program becomes [quite challenging on MacOS and Windows machines](https://medium.com/@jijupax/connect-the-webcam-to-docker-on-mac-or-windows-51d894c44468).

### Using docker
#### Requirements
- Docker
- [.env file](#environment-variables)

```bash
# Run the lastest version (docker image)
$ ./client.sh
# Or
$ ./client.sh latest .env

# Run a specific version (e.g., 0.0.1) and specific env file (e.g., local.env)
$ ./client.sh 0.0.1 local.env
```
View all available docker images on the [Docker Hub repository](https://hub.docker.com/repository/docker/caloverflow/security-system-client). 

### Using Python virtualenv
#### Requirements
- Python 3.9 or 3.10
- pip
- [.env file](#environment-variables)

#### Install dependencies in virtualenv
```bash
$ python -m venv ./venv

# Activate the virtual environment
$ source ./venv/bin/activate
$ pip install -r requirements.txt

# Run the script
$ python src/main.py
```

#### Environment variables
The following environment variables are used by the client. It is recommended that these values are placed within a `.env` file.

| Variable | Default | Purpose | Required |
| :-: | :-: | :--|
| `REGION` | - | The AWS region in which your AWS resources are located. An example is `us-east-1` | ✅ |
| `S3_BUCKET` | - | The name of the unique S3 bucket to which clips should be synced. | ✅ |
| `AWS_ACCESS_KEY_ID` | - | The ID of the access key that is to be used for authenticating requests to AWS services (S3). | ✅ |
| `AWS_SECRET_ACCESS_KEY` | - | The secret access key that is to be used for authenticating requests to AWS services (S3). | ✅ |
| `CAMERA_NAME` | - | The name of the camera used in identifying the origin of clips. If no value is provided, a unique identifier is generated. | ❌ |
| `CLIP_LENGTH` | `30` | The length, in seconds, that clips should be saved. | ❌ |
| `OUTPUT_PATH` | `./tmp` | The path to the folder where video clips should be saved. Note - this is not currently supported for the Docker configuration. | ❌ |

To make things simpler, you may copy this base `.env` file and fill out the environment variables as needed.
```
# Required
REGION=
S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Optional
CAMERA_NAME=
CLIPS_PER_UPLOAD=
CLIP_LENGTH=
```

Pass the environment variables via the command line:
##### Docker

```bash
$ ./client.sh 

# With parameters
# specific tag version (default environment variable file)
$ ./client.sh 0.0.1
# latest tag + specific environment variable file
$ ./client.sh latest local.env
# specific tag + specific environment variable file
$ ./client.sh 0.0.1 local.env
```
Argument 1 is the specific image tag version. Default value of `latest`. \
Argument 2 is the path to the environment variable file. Default value of `.env`.

##### Python command line
The `.env` file will be automatically picked up by the python program given it is located in the base directory.
```bash
$ python src/main.py
```


### Deploying
To deploy the Cloudformation stack with all necessary AWS resources, simply add a
### 1. Create an IAM Role
In your AWS Account, create a new IAM Role with the permissions you deem necessary. This must include [Cloudformation](https://aws.amazon.com/cloudformation/) and [S3](https://aws.amazon.com/ec2/). Refer to GitHub's docs for [Configuring OpenID Connect in AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) for guidance.

### 2. Add essential secrets to your GitHub repository.

Add the following secrets via **Repository settings** > **Secrets** > **Actions**.

  - `IAM_ROLE_ARN` containing your IAM Role ARN from step 1.

### 3. Trigger a deploy
To trigger a deploy, simply commit changes to the `main` branch. You may also trigger a deploy within the **Actions** tab on the repository.

