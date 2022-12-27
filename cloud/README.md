# serverless-security-system
## Cloud
Cloud computing resources (such as AWS Lambda) run and process the footage recorded by each [client](../cloud/README.md).

# TODO
TODO - explain the cloud architecture

# Configuration
The system configuration is maintained within the `settings.json` file. This file is copied to S3 when the cloud deploy is triggered. The values for the configuration are:

- `is_motion_outlined` - Whether or not motion should be outlined
- `clip_length` - The length that clips should be recorded
- `clips_per_upload` - The number of clips to record between uploads
- `default_motion_threshold` - The default motion threshold for cameras. Clients ignore this value after their configuration file is generated (happens after the first upload is completed)
- `days_to_keep_motionless_videos` - The number of days to keep videos that do not include motion. Note that making this value greater than 365 may make it difficult to later update the value (i.e., changing from 1000 to 30 can cause lambda timeout when trying to purge all files between 1000 days ago and 30 days ago).

# Backend
To view the various API endpoints, view [api-endpints.md](./api-endpoints.md).

