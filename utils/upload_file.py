import logging
import boto3
from botocore.exceptions import ClientError
from decouple import config


def upload_file_object(file_obj, bucket, key):
    """Upload a file to an S3 bucket

    :param file_obj:  A file-like object to upload. At a minimum, it must implement the read method, and must return bytes.
    :param bucket: Bucket to upload to
    :param key: name of key to upload to
    :param callback_fxn: function to process response after upload
    :return: true if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(file_obj, bucket, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_presigned_url(bucket_name, key, expiration=3600):
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.info('TEST RUN STARTED')
    test_file = 'test.png'
    BUCKET_NAME = config('S3_BUCKET_NAME')
    KEY_NAME = 'apps/bs/test.png'


    with open(test_file, 'rb') as image:
        response = upload_file_object(
            file_obj=image,
            bucket=BUCKET_NAME,
            key=KEY_NAME,
        )

        if response:
            print("Successful")
        print("Failed", response)

    logger.info('TEST RUN COMPLETED')
    