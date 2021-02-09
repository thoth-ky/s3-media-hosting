from decouple import config

BUCKET_NAME = config('S3_BUCKET_NAME')
ROOT_FOLDER = config('ROOT_FOLDER', default='apps')