import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import librosa
import soundfile as sf

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

class PreviewService:

    @staticmethod
    def generate_variants(data: bytes, file_type: str) -> tuple[bytes, bytes]:
        if file_type and file_type.startswith("image/"):
            return PreviewService._image_variants(data)
        if file_type and file_type.startswith("audio/"):
            return PreviewService._audio_variants(data)
        if file_type == "application/pdf":
            return PreviewService._document_variants(data)
        return None, data

    @staticmethod
    def _apply_tiled_watermark(base: Image.Image, watermark_text: str) -> Image.Image:
        overlay = Image.new('RGBA', base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        font_size = int(min(base.size) * 0.05)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        padding = int(font_size * 0.2)
        pw, ph = text_w + 2 * padding, text_h + 2 * padding
        cos45 = math.cos(math.radians(45))
        sin45 = math.sin(math.radians(45))
        rw = int(abs(pw * cos45) + abs(ph * sin45))
        rh = int(abs(pw * sin45) + abs(ph * cos45))
        step = max(rw, rh) * 1.2
        fill = (64, 64, 64, 160)
        for y in range(-rh, base.height + rh, int(step)):
            for x in range(-rw, base.width + rw, int(step)):
                txt_img = Image.new('RGBA', (pw, ph), (255, 255, 255, 0))
                td = ImageDraw.Draw(txt_img)
                td.text((padding, padding), watermark_text, fill=fill, font=font)
                rot = txt_img.rotate(45, expand=True)
                ox, oy = x - rot.width // 2, y - rot.height // 2
                overlay.paste(rot, (ox, oy), rot)
        return Image.alpha_composite(base.convert('RGBA'), overlay)

    @staticmethod
    def _image_variants(data: bytes) -> tuple[bytes, bytes]:
        img = Image.open(BytesIO(data)).convert('RGBA')
        fmt = img.format or 'PNG'
        # thumbnail з водяним знаком
        thumb = img.copy()
        thumb.thumbnail((200, 200))
        thumb_wm = PreviewService._apply_tiled_watermark(thumb, '© One4Lib')
        buf_t = BytesIO();
        thumb_wm.save(buf_t, format=fmt)
        thumb_bytes = buf_t.getvalue()
        # preview з водяним знаком
        prev = img.copy()
        prev.thumbnail((800, 800))
        prev_wm = PreviewService._apply_tiled_watermark(prev, '© One4Lib')
        buf_p = BytesIO();
        prev_wm.convert('RGB').save(buf_p, format=fmt)
        prev_bytes = buf_p.getvalue()
        return thumb_bytes, prev_bytes

    @staticmethod
    def _audio_variants(data: bytes) -> tuple[bytes, bytes]:
        # завантажуємо повне аудіо
        y, sr = librosa.load(BytesIO(data), sr=None)
        total_samples = len(y)
        # довжина прев'ю: 20% від загального часу, від 1 до 15 секунд
        duration_sec = clamp(total_samples / sr * 0.2, 1, 15)
        snippet_samples = int(duration_sec * sr)
        snippet = y[:snippet_samples]
        # експорт у WAV
        buf_audio = BytesIO()
        sf.write(buf_audio, snippet, sr, format='WAV')
        preview_audio = buf_audio.getvalue()
        # thumbnail — сіра кнопка "Play"
        thumb = Image.new('RGB', (200, 200), color='gray')
        draw = ImageDraw.Draw(thumb)
        triangle = [(80, 60), (80, 140), (140, 100)]
        draw.polygon(triangle, fill='white')
        buf_t = BytesIO();
        thumb.save(buf_t, format='PNG')
        thumb_bytes = buf_t.getvalue()
        return thumb_bytes, preview_audio

    @staticmethod
    def _document_variants(data: bytes) -> tuple[bytes, bytes]:
        """
        Генерує thumbnail (PNG) та preview (PDF) для PDF-документів.
        Preview — новий PDF з водяними знаками, thumbnail — зображення першої сторінки.
        """
        if not HAS_PYMUPDF:
            raise RuntimeError('PyMuPDF required')

        # Відкриваємо оригінал
        doc = fitz.open(stream=data, filetype='pdf')
        total = doc.page_count
        # Вибираємо 20% сторінок, мінімум 1, максимум 5
        count = clamp(int(total * 0.2), 1, 5)
        idxs = [min(int(i * total / count), total - 1) for i in range(count)]

        # Створюємо новий PDF з водяними знаками
        new_pdf = fitz.open()
        for idx in idxs:
            pg = doc.load_page(idx)
            pix = pg.get_pixmap(matrix=fitz.Matrix(150 / 72, 150 / 72))
            base = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).convert('RGBA')
            wm = PreviewService._apply_tiled_watermark(base, '© One4Lib')

            npg = new_pdf.new_page(width=pix.width, height=pix.height)
            buf_img = BytesIO()
            wm.convert('RGB').save(buf_img, format='PNG')
            npg.insert_image(fitz.Rect(0, 0, pix.width, pix.height), stream=buf_img.getvalue())

        # Зберігаємо новий PDF у буфер
        buf_pdf = BytesIO()
        new_pdf.save(buf_pdf)
        pdf_bytes = buf_pdf.getvalue()

        # Генеруємо thumbnail: перша сторінка preview PDF
        preview_doc = fitz.open(stream=pdf_bytes, filetype='pdf')
        p0 = preview_doc.load_page(0)
        p0pix = p0.get_pixmap(matrix=fitz.Matrix(200 / 72, 200 / 72))
        thumb_img = Image.frombytes('RGB', (p0pix.width, p0pix.height), p0pix.samples)
        thumb_img.thumbnail((200, 200))

        buf_thumb = BytesIO()
        thumb_img.save(buf_thumb, format='PNG')
        thumb_bytes = buf_thumb.getvalue()

        return thumb_bytes, pdf_bytes
