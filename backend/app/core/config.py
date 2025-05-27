from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str = Field(..., env="MONGO_URI")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 1440

    aws_access_key_id:     str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_bucket_name:       str = Field(..., env="AWS_BUCKET_NAME")
    aws_region:            str = Field(..., env="AWS_REGION")
    aws_signature_version: str = Field("s3v4", env="AWS_SIGNATURE_VERSION")

    class Config:
        env_file = ".env"

settings = Settings()
