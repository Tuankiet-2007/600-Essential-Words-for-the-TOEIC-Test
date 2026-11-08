"""
Script 2: batch_ocr_to_json.py
Tác dụng:
Gửi 6 ảnh scan của từng Lesson (rất nhẹ, chỉ ~300KB/bài) lên Gemini 2.5 Flash API
để tự động đọc OCR + dịch nghĩa tiếng Việt + xuất ra file JSON chuẩn cấu trúc của lesson_01.json.
Bằng cách chia nhỏ từng Lesson (6 trang/lần gọi), AI tuyệt đối không bị quá tải hay sót chữ!

Cài đặt thư viện trước khi chạy:
    pip install google-genai pillow
"""

import os
import json
import time
from PIL import Image
from google import genai
from google.genai import types

# Điền Gemini API Key của bạn vào đây (hoặc set biến môi trường GEMINI_API_KEY)
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

def process_lesson(client, lesson_meta, sample_schema_str, scans_root, out_dir):
    lid = lesson_meta["lesson_id"]
    out_file = os.path.join(out_dir, f"lesson_{lid:02d}.json")
    if os.path.exists(out_file):
        print(f"Lesson {lid:02d} đã tồn tại, bỏ qua...")
        return

    lesson_scan_dir = os.path.join(scans_root, f"lesson_{lid:02d}")
    image_files = sorted(os.listdir(lesson_scan_dir))
    images = [Image.open(os.path.join(lesson_scan_dir, f)) for f in image_files if f.endswith(".png")]

    prompt = f"""
Bạn là hệ thống số hóa sách TOEIC chính xác tuyệt đối.
Đây là 6 trang scan của Lesson {lid}: "{lesson_meta['title']}" thuộc chủ đề "{lesson_meta['theme_name']}".
Hãy trích xuất toàn bộ nội dung trên 6 trang này và trả về đúng định dạng JSON Schema mẫu bên dưới.
Yêu cầu bắt buộc:
1. Trích xuất đủ 12 từ vựng mục tiêu trong phần WORDS TO LEARN, tự động bổ sung phiên âm IPA, nghĩa tiếng Việt sát ngữ cảnh TOEIC, collocations trong bài và dịch 2 câu ví dụ a, b sang tiếng Việt.
2. Ghép phần WORD FAMILIES vào đúng từ vựng tương ứng trong mảng `words_to_learn`.
3. Trích xuất chính xác đoạn văn `words_in_context` và điền sẵn đáp án đúng cho 12 ô trống.
4. Trích xuất toàn bộ câu hỏi Listening (Part 1, 2, 3, 4) và Reading (Part 5, 6, 7) kèm đáp án đúng cho Part 5, 6, 7.

Cấu trúc JSON mẫu (hãy tuân thủ 100% tên các trường):
{sample_schema_str}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[*images, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"[THÀNH CÔNG] Đã xuất {out_file}")

def main():
    client = genai.Client(api_key=API_KEY)
    with open("book_structure_map.json", "r", encoding="utf-8") as f:
        book_map = json.load(f)
    with open("sample_lessons/lesson_01.json", "r", encoding="utf-8") as f:
        sample_schema_str = f.read()

    scans_root = os.path.join("extracted_data", "lesson_page_scans")
    out_dir = "lessons_json"
    os.makedirs(out_dir, exist_ok=True)

    for lesson_meta in book_map["lessons"]:
        process_lesson(client, lesson_meta, sample_schema_str, scans_root, out_dir)
        time.sleep(2) # Tránh vượt quá rate limit

if __name__ == "__main__":
    main()
