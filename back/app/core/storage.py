# app/core/storage.py
import uuid
import boto3
from botocore.client import Config
from .config import settings

# Ініціалізуємо S3-клієнт з параметрами з Settings
s3 = boto3.client(
    "s3",
    aws_access_key_id     = settings.aws_access_key_id,
    aws_secret_access_key = settings.aws_secret_access_key,
    region_name           = settings.aws_region,
    config                = Config(signature_version=settings.aws_signature_version),
)

def upload_fileobj(file_obj, content_type: str) -> str:
    key = f"uploads/{uuid.uuid4()}"
    s3.upload_fileobj(
        Fileobj   = file_obj,
        Bucket    = settings.aws_bucket_name,
        Key       = key,
        ExtraArgs = {"ContentType": content_type, "ACL": "private"},
    )
    return key

def create_signed_url(key: str, expires: int = 300) -> str:
    return s3.generate_presigned_url(
        ClientMethod = "get_object",
        Params       = {"Bucket": settings.aws_bucket_name, "Key": key},
        ExpiresIn    = expires,
    )
