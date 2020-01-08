# data-workflow (under development)

Internal web application for managing data and data workflow. 

Includes some utilities for: 
- checking for duplicate files within object storage buckets
- deletion of duplicate files within object storage buckets

With this application we aim to be able to manage all data files, datasets and outputs, resulting in an overseen workflow for managing data.

## How to use this software

### Set up (TODO)

### Importing buckets and file lists

Import a list of all buckets into the database.

importbucketlist.py

To create a list of files in a bucket, use a tool such as ls (or similar - see manual) from rclone https://rclone.org/, or list_s3_files.py from https://github.com/Swiss-Polar-Institute/data-copy-verification Then import this list of all files in a bucket into the database (the list will need to match the details required).

importbucketfilelist.py

See the database ER diagram (TODO) for details of what information is included. 

### Checking for duplicate files within a bucket



