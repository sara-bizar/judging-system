import pytest
from project import law_analyzer

test_cases = [
    ("ورود غیرمجاز به سیستم رایانه‌ای باید جرم باشد.", "ماده 1"),
    ("دسترسی غیرمجاز به داده‌های در حال انتقال غیرقانونی است.", "ماده 2"),
    ("اگر کسی اطلاعات ذخیره شده را تغییر دهد، مجازات دارد.", "ماده 3"),
    ("حذف اطلاعات دیگران بدون اجازه ممنوع است.", "ماده 4"),
    ("جمع‌آوری اطلاعات خصوصی مردم بدون اجازه نباید مجاز باشد.", "ماده 5")
]

@pytest.mark.parametrize("input_text, expected_article", test_cases)
def test_law_matching(input_text, expected_article):
    result = law_analyzer.analyze_text(input_text)
    matched_article = result["matched"]["article"]
    
    # فقط بررسی می‌کنیم که ابتدای متن با ماده مورد نظر شروع میشه
    assert matched_article.startswith(expected_article), f"Expected article starting with '{expected_article}', got '{matched_article}'"
