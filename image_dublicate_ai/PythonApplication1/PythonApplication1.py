import os
import glob
import imagehash
from PIL import Image
from itertools import combinations
from openpyxl import Workbook
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import time

# === Налаштування ===
INPUT_DIR = "images"  # директорія з зображеннями
MAX_DISTANCE = 10     # поріг відстані Хеммінга для схожих зображень
OUTPUT_EXCEL = "similar_images.xlsx"

# Еталонні правильні пари (за потреби — заповнити)
TRUE_MATCHES = {
    ("112243673_fd68255217.jpg", "112243673_fd68255217 – копія.jpg"),
    ("118187095_d422383c81.jpg", "118187095_d422383c81 – копія.jpg"),
    ("56489627_e1de43de34.jpg", "56489627_e1de43de34 – копія.jpg"),
    ("96978713_775d66a18d.jpg", "96978713_775d66a18d – копія.jpg")
}


def get_image_paths(input_dir):
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.bmp')
    paths = []
    for ext in extensions:
        paths.extend(glob.glob(os.path.join(input_dir, ext)))
    return paths


def compute_hash(image_path):
    try:
        img = Image.open(image_path).convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        return image_path, imagehash.dhash(img)
    except Exception as e:
        print(f"❌ Error with {image_path}: {e}")
        return image_path, None


def compare_pair(pair):
    (path1, hash1), (path2, hash2) = pair
    if hash1 is None or hash2 is None:
        return None
    dist = hash1 - hash2
    if dist <= MAX_DISTANCE:
        return (os.path.basename(path1), os.path.basename(path2), dist)
    return None


def normalize(pair):
    return tuple(sorted(pair))


def analyze_with_threads(thread_count):
    start_time = time.time()

    print(f"🔍 Пошук зображень... ({thread_count} потоків)")
    image_paths = get_image_paths(INPUT_DIR)
    print(f"Знайдено {len(image_paths)} зображень.")

    print("🔢 Обчислення хешів...")
    with Pool(processes=thread_count) as pool:
        hashes = pool.map(compute_hash, image_paths)

    print("📊 Порівняння всіх пар...")
    pairs = list(combinations(hashes, 2))
    with Pool(processes=thread_count) as pool:
        results = list(tqdm(pool.imap(compare_pair, pairs), total=len(pairs)))

    similar = [r for r in results if r is not None]

    print(f"✅ Знайдено {len(similar)} пар схожих зображень (відстань ≤ {MAX_DISTANCE})")

    print("💾 Збереження в Excel...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Similar Images"
    ws.append(["Image 1", "Image 2", "Hamming Distance"])

    for row in similar:
        ws.append(row)

    wb.save(OUTPUT_EXCEL)
    print(f"📁 Збережено у файл: {OUTPUT_EXCEL}")

    # === Метрики ефективності ===
    found_pairs = {normalize((a, b)) for a, b, _ in similar}
    true_pairs = {normalize(p) for p in TRUE_MATCHES}

    TP = len(found_pairs & true_pairs)
    FP = len(found_pairs - true_pairs)
    FN = len(true_pairs - found_pairs)

    precision = TP / (TP + FP) if TP + FP > 0 else 0
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    throughput = len(image_paths) / elapsed

    print("\n📊 Підсумкова статистика:")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-score:  {f1:.3f}")
    print(f"Час обробки: {minutes} хв {seconds} сек")
    print(f"Пропускна здатність: ~{int(throughput)} зображень/сек")


def main():
    # Список різних значень потоків для тестування
    thread_counts = [1, 2, 4, 8, 16]

    for thread_count in thread_counts:
        analyze_with_threads(thread_count)


if __name__ == "__main__":
    main()
