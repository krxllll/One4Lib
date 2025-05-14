# app/files/preview_utils.py
import io
import uuid
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from botocore.exceptions import ClientError
from app.core.storage import s3, settings, create_signed_url


async def generate_image_preview(
    source_key: str,
    size: tuple[int, int] = (200, 200),
    watermark_text: Optional[str] = None
) -> str:
    """
    Створює зображення-прев'ю (thumbnail) з оригінального об'єкта у S3,
    накладає необов'язковий ватермарк та повертає signed URL на прев'ю.
    """
    # 1. Завантажуємо оригінал з S3
    try:
        obj = s3.get_object(Bucket=settings.aws_bucket_name, Key=source_key)
        data = obj['Body'].read()
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch source object: {e}")

    # 2. Створюємо thumbnail
    img = Image.open(io.BytesIO(data))
    img.thumbnail(size)

    # 3. Додаємо ватермарк (якщо задано)
    if watermark_text:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text_size = draw.textsize(watermark_text, font=font)
        position = (img.width - text_size[0] - 5, img.height - text_size[1] - 5)
        draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    # 4. Зберігаємо прев'ю назад у S3 під окремим ключем
    buffer = io.BytesIO()
    img_format = 'JPEG' if img.format != 'PNG' else 'PNG'
    img.save(buffer, format=img_format)
    buffer.seek(0)

    preview_key = f"previews/{uuid.uuid4()}.{img_format.lower()}"
    try:
        s3.upload_fileobj(
            Fileobj=buffer,
            Bucket=settings.aws_bucket_name,
            Key=preview_key,
            ExtraArgs={
                "ContentType": f"image/{img_format.lower()}",
                "ACL": "private",
            },
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to upload preview object: {e}")

    # 5. Генеруємо signed URL на прев'ю
    return create_signed_url(preview_key)
