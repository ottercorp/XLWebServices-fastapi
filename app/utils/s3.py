import boto3
from botocore.client import Config

from logs import logger
from ..config import Settings


def create_client(settings: Settings):
    s3_config = {
        'access_key': settings.xivlauncher_s3_access_key,
        'secret_key': settings.xivlauncher_s3_secret_key,
        'endpoint': settings.xivlauncher_s3_endpoint,
    }
    missing = [key for key, value in s3_config.items() if not value]
    if len(missing) == 3:
        logger.info("S3 config is empty, skipping upload.")
        return
    if missing:
        raise RuntimeError(f"Incomplete S3 config: {', '.join(missing)}")

    return boto3.client(
        's3',
        endpoint_url=settings.xivlauncher_s3_endpoint,
        aws_access_key_id=settings.xivlauncher_s3_access_key,
        aws_secret_access_key=settings.xivlauncher_s3_secret_key,
        region_name='auto',
        config=Config(s3={'addressing_style': 'path'}),
    )


def upload_file(client, file_path: str, bucket: str, object_key: str):
    logger.info(f"Uploading {file_path} -> s3://{bucket}/{object_key}")
    client.upload_file(file_path, bucket, object_key)
