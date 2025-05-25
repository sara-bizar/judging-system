from flask import Flask, render_template, request
from project import law_analyzer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    references = []
    score = None

    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            analysis = law_analyzer.analyze_text(user_input)
            result = analysis["matched"]
            references = analysis["references"]
            score = analysis["score"]
    # اگر GET باشه، متغیرها همون مقادیر اولیه می‌مونن (None و [])
    
    return render_template("index.html", result=result, references=references, score=score)


if __name__ == "__main__":
    app.run(debug=True)

