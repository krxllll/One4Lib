import mimetypes
import math
from pathlib import Path
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
                txt_img = Image.new('RGBA', (pw, ph), (255,255,255,0))
                td = ImageDraw.Draw(txt_img)
                td.text((padding, padding), watermark_text, fill=fill, font=font)
                rot = txt_img.rotate(45, expand=True)
                ox, oy = x - rot.width//2, y - rot.height//2
                overlay.paste(rot, (ox, oy), rot)
        return Image.alpha_composite(base.convert('RGBA'), overlay)

    @staticmethod
    def _make_square_thumb(img: Image.Image, size: int = 512) -> Image.Image:
        """
        З масштабує (якщо оригінал менший за size) або кропає центр
        (якщо оригінал більший за size) до квадрату size×size.
        """
        w, h = img.size
        # 1) масштаб up, якщо хоча б одна сторона менша за size
        if w < size or h < size:
            scale = size / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        # 2) тепер img >= size×size в обох вимірах — вирізаємо центр
        left = (img.width - size) // 2
        top = (img.height - size) // 2
        return img.crop((left, top, left + size, top + size))

    @staticmethod
    def _image_variants(data: bytes) -> tuple[bytes, bytes]:
        img = Image.open(BytesIO(data)).convert('RGBA')
        fmt = img.format or 'PNG'

        # --- квадратний thumbnail 512×512 ---
        thumb_sq = PreviewService._make_square_thumb(img, 512)
        # накладаємо watermark так само, як і раніше
        thumb_wm = PreviewService._apply_tiled_watermark(thumb_sq, '© One4Lib')
        buf_t = BytesIO()
        thumb_wm.save(buf_t, format=fmt)
        thumb_bytes = buf_t.getvalue()

        # --- preview з максимальною стороною 800 ---
        prev = img.copy()
        prev.thumbnail((800, 800), Image.LANCZOS)
        prev_wm = PreviewService._apply_tiled_watermark(prev, '© One4Lib')
        buf_p = BytesIO()
        prev_wm.convert('RGB').save(buf_p, format=fmt)
        prev_bytes = buf_p.getvalue()

        return thumb_bytes, prev_bytes

    @staticmethod
    def _audio_variants(data: bytes) -> tuple[bytes, bytes]:
        y, sr = librosa.load(BytesIO(data), sr=None)
        total = len(y)
        dur = clamp(total / sr * 0.2, 1, 15)
        snippet = y[: int(dur * sr)]
        buf_wav = BytesIO();
        sf.write(buf_wav, snippet, sr, format='WAV')
        wav_bytes = buf_wav.getvalue()

        # → thumbnail 512×512 с Play-кнопкой
        thumb = Image.new('RGB', (512, 512), color='gray')
        draw = ImageDraw.Draw(thumb)
        # масштабируем старые координаты 200→512
        scale = 512 / 200
        triangle = [
            (int(80 * scale), int(60 * scale)),
            (int(80 * scale), int(140 * scale)),
            (int(140 * scale), int(100 * scale)),
        ]
        draw.polygon(triangle, fill='white')
        buf_t = BytesIO();
        thumb.save(buf_t, format='PNG')
        return buf_t.getvalue(), wav_bytes

    @staticmethod
    def _document_variants(data: bytes) -> tuple[bytes, bytes]:
        """
        Повертає (thumbnail_bytes, preview_pdf_bytes) для PDF.
        Thumbnail — квадрат 512×512, із масштабуванням або кропом центру.
        Preview — новий PDF з водяними знаками.
        """
        if not HAS_PYMUPDF:
            raise RuntimeError('PyMuPDF required')

        # 1) Рендеримо новий PDF з водяними знаками
        doc = fitz.open(stream=data, filetype='pdf')
        total = doc.page_count
        count = clamp(int(total * 0.2), 1, 5)
        idxs = [min(int(i * total / count), total - 1) for i in range(count)]
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
        buf_pdf = BytesIO()
        new_pdf.save(buf_pdf)
        pdf_bytes = buf_pdf.getvalue()

        # 2) Генеруємо квадратний thumbnail 512×512 із першої сторінки водяного PDF
        preview_doc = fitz.open(stream=pdf_bytes, filetype='pdf')
        p0 = preview_doc.load_page(0)
        p0pix = p0.get_pixmap(matrix=fitz.Matrix(200 / 72, 200 / 72))
        thumb_img = Image.frombytes('RGB', (p0pix.width, p0pix.height), p0pix.samples)
        # Перетворюємо в RGBA для сумісності (якщо треба)
        thumb_img = thumb_img.convert('RGBA')

        # Обрізаємо або масштабуємо/кропаємо до квадрату 512×512
        thumb_sq = PreviewService._make_square_thumb(thumb_img, 512)
        buf_t = BytesIO()
        thumb_sq.save(buf_t, format='PNG')
        thumb_bytes = buf_t.getvalue()

        return thumb_bytes, pdf_bytes


def process_file(input_path: Path, output_dir: Path):
    mime,_ = mimetypes.guess_type(input_path)
    if mime is None:
        print(f'[WARN] Unknown MIME for {input_path.name}')
        return
    data = input_path.read_bytes()
    thumb, prev = PreviewService.generate_variants(data,mime)
    stem, ext = input_path.stem, input_path.suffix.lstrip('.')
    # для аудіо прев'ю збережемо як WAV
    prev_ext = 'wav' if mime.startswith('audio/') else ext
    tpath = output_dir / f"{stem}_{ext}_thumbnail.png"
    ppath = output_dir / f"{stem}_{ext}_preview.{prev_ext}"
    output_dir.mkdir(parents=True, exist_ok=True)
    if thumb:
        tpath.write_bytes(thumb)
        print(f'Thumbnail saved: {tpath}')
    if prev:
        ppath.write_bytes(prev)
        print(f'Preview saved: {ppath}')

PROJECT_ROOT = Path(__file__).parents[3]
TEST_DIR = PROJECT_ROOT / 'tests'
TEST_FILES = [TEST_DIR/'sample.png', TEST_DIR/'sample.pdf', TEST_DIR/'sample.mp3']
OUTPUT_DIR = PROJECT_ROOT / 'results'
if __name__=='__main__':
    for p in TEST_FILES:
        if not p.exists(): print(f'[ERROR] Not found: {p}'); continue
        process_file(p, OUTPUT_DIR)
    print('Processing completed.')
