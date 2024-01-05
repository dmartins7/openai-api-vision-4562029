import base64
import json
from io import BytesIO

from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/vision", methods=["POST"])
def vision():
    """api endpoint"""
    if "file" not in request.files:
        return "No file part in the request", 400
    file = request.files["file"]
    item_list = json.loads(request.form.get("userItems", "[]"))
    if not item_list:
        return jsonify(
            ["Please enter items that are supposed to be in the refrigerator"]
        )
    prompt = f"""Which of the following grocery items are missing? Soy milk, chocolate pudding, apples. Response should be a list of items that are missing. ["missing item1", "missing item2", "missing item3"]"""
    print(prompt)
    file_content = file.read()
    base64_image = base64.b64encode(file_content).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
