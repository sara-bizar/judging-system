import re
import json

with open('law.txt', 'r', encoding='utf-8') as file:
    text = file.read()

pattern = r"(ماده\s*(\d+)\s*[-ـ]?\s.*?)(?=\n\s*ماده\s*\d+\s*[-ـ]?|\Z)"
matches = re.findall(pattern, text, flags=re.DOTALL)

articles = []
for idx, (full_match, number) in enumerate(matches, start=1):
    # حذف خطوطی که با "فصل" یا "مبحث" شروع می‌شوند
    cleaned_lines = []
    for line in full_match.split('\n'):
        line_strip = line.strip()
        if not (line_strip.startswith('فصل') or line_strip.startswith('مبحث')):
            cleaned_lines.append(line)
    cleaned_text = '\n'.join(cleaned_lines).strip()

    # حذف عنوان "ماده X" از متن
    text_body = re.sub(r'^ماده\s*\d+\s*[-ـ]?', '', cleaned_text).strip()

    articles.append({
        "id": idx,
        "text": text_body,
        "article": f"ماده {number} قانون جرایم رایانه‌ای"
    })

with open('articles.json', 'w', encoding='utf-8') as json_file:
    json.dump(articles, json_file, ensure_ascii=False, indent=2)

print("✅ ماده‌ها در قالب ساختار دلخواه ذخیره شدند.")


