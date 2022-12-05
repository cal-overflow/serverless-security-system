# serverless-security-system
A serverless security system built with AWS Services
**NOTE: This project is a work in progress**

### Some notes
**This security system sacrifices video livestreaming for the benefit of a serverless (more affordable) architecture.** Additionally, the removal of livestreaming allows for less cpu requirements of each camera, and in turn a better video capture.

#### Archicture (tentative)

##### Client
A "Client" is more-or-less a camera + computer that has the purpose of recording footage and periodically sending it to the cloud storage. \
Little or no video processing is done at the client-side to allow "weak" computers (such as a raspberry pi) to act as the client.

See more in the [Client README](./client/README.md).

##### Cloud
Cloud computing resources (such as AWS Lambda) run and process the footage recorded by each client. \
The most essential resources are:
- S3 - store videos uploaded by clients
- Lambda - Process videos in S3. Remove videos that are not important (i.e., do not have any motion)

See more in the [Cloud README](./cloud/README.md).

##### Misc notes
- Docker-based client "application" that records footage of x min intervals.
- Some kind of authentication will be needed so that setting up a client to have permissions to upload files to S3 bucket.
- CRON-interval processes where the "client" syncs the footage to an S3 bucket.
- CRON-interval processes at the cloud-level where footage is "processed" and potentially disposed.

### Deploying
To deploy the Cloudformation stack with all necessary AWS resources, simply add a
### 1. Create an IAM Role
In your AWS Account, create a new IAM Role with the permissions you deem necessary. This must include [Cloudformation](https://aws.amazon.com/cloudformation/) and [S3](https://aws.amazon.com/ec2/). Refer to GitHub's docs for [Configuring OpenID Connect in AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) for guidance.

### 2. Add essential secrets to your GitHub repository.

Add the following secrets via **Repository settings** > **Secrets** > **Actions**.

  - `IAM_ROLE_ARN` containing your IAM Role ARN from step 1.

### 3. Trigger a deploy
To trigger a deploy, simply commit changes to the `main` branch. You may also trigger a deploy within the **Actions** tab on the repository.

