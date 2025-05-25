import json
import re
import os
import torch
from sentence_transformers import SentenceTransformer, util

# بارگذاری مدل
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# بارگذاری مواد قانونی
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "articles.json")

with open(json_path, "r", encoding="utf-8") as f:
    laws = json.load(f)

# ساخت map از id برای دسترسی سریع
law_by_id = {law['id']: law for law in laws}

# بررسی وجود فایل embedding
embedding_file = "law_embeddings.pt"

if os.path.exists(embedding_file):
    law_embeddings = torch.load(embedding_file)
else:
    law_texts = [law['text'] for law in laws]
    law_embeddings = model.encode(law_texts, convert_to_tensor=True)
    torch.save(law_embeddings, embedding_file)

# تابع استخراج ارجاع به شماره ماده‌ها (پرانتزدار)
def find_article_references(text, current_id):
    matches = re.findall(r"\((\d{1,3})\)", text)
    references = [int(m) for m in matches if int(m) != current_id]
    return references

# تابع اصلی برای استفاده در وب

def analyze_text(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.cos_sim(user_embedding, law_embeddings)
    best_match_idx = torch.argmax(cosine_scores).item()
    matched_law = laws[best_match_idx]

    refs = find_article_references(matched_law['text'], matched_law['id'])
    ref_laws = [law_by_id[ref_id] for ref_id in refs if ref_id in law_by_id]

    return {
        "matched": {
            "article": matched_law['article'],
            "text": matched_law['text']
        },
        "score": cosine_scores[0][best_match_idx].item(),
        "references": ref_laws
    }
