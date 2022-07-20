import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse
from dataclasses import dataclass


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

@dataclass
class S3UploadInfo:
    filename_source: str
    filename_target: str
    bucketname: str


def get_input() -> S3UploadInfo:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    parser.add_argument('bucket', type=str)

    args = parser.parse_args()

    return S3UploadInfo(
        filename_target=args.target,
        filename_source=args.source,
        bucketname=args.bucket,
    )

if __name__=="__main__":
    input_ = get_input()
    upload_file(input_.filename_source, input_.bucketname, input_.filename_target)